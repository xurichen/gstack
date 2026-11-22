#!/usr/bin/env python3
"""Deterministic evaluation scorer for the gardener loop.

Separates agent task generation from scoring so agents never grade their own
pass/fail status or write directly to evals/results/.

Stdlib only (Python 3.9+). Run `python3 scripts/score-eval.py --self-test` to
verify every verdict branch.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

REQUIRED_HEADER_KEYS = ("source", "date", "task_id", "expected_output_note")
TEMPLATE_SENTINEL = "TEMPLATE_NOT_REAL_DATA"
NOISE_FLOOR_PCT = 5.0
COST_GUARDRAIL_RATIO = 2.0


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def get_git_sha(repo_root: Path) -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(repo_root),
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return out or "untracked"
    except Exception:
        return "untracked"


def parse_md_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---", text)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        result[k.strip()] = v.strip().strip('"').strip("'")
    return result


def validate_human_data_file(path: Path, expected_task_id: str) -> tuple[bool, str]:
    if not path.exists() or not path.is_file():
        return False, f"missing file: {path}"
    raw = path.read_text(encoding="utf-8", errors="replace")
    if TEMPLATE_SENTINEL in raw:
        return False, f"template placeholder found in {path.name}"
    header: dict[str, Any]
    if path.suffix == ".json":
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            return False, f"invalid JSON in {path.name}: {exc}"
        header = payload.get("_header", {}) if isinstance(payload, dict) else {}
    else:
        header = parse_md_frontmatter(raw)
    missing = [k for k in REQUIRED_HEADER_KEYS if not str(header.get(k, "")).strip()]
    if missing:
        return False, f"missing header keys {missing} in {path.name}"
    if str(header.get("task_id", "")).strip() != expected_task_id:
        return False, f"task_id mismatch in {path.name}: expected {expected_task_id}"
    return True, "ok"


def check_suite_human_data(data_dir: Path, tasks: list[dict[str, Any]]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    human_tasks = [t for t in tasks if t.get("tier") == "human"]
    for task in human_tasks:
        tid = task["id"]
        if not data_dir.exists():
            errors.append(f"human data directory missing: {data_dir}")
            continue
        candidates = [
            p for p in sorted(data_dir.iterdir())
            if p.is_file()
            and not p.name.startswith("_template")
            and p.name.startswith(f"{tid}-")
            and p.suffix in (".json", ".md")
        ]
        if not candidates:
            errors.append(f"no human data file for Tier 1 task '{tid}' in {data_dir}")
            continue
        for c in candidates:
            ok, msg = validate_human_data_file(c, tid)
            if not ok:
                errors.append(msg)
    return len(errors) == 0, errors


def metric_delta_pct(new_val: float | None, old_val: float | None) -> float | None:
    if new_val is None or old_val is None:
        return None
    if old_val == 0:
        return 0.0 if new_val == 0 else (100.0 if new_val > 0 else -100.0)
    return round(((new_val - old_val) / abs(old_val)) * 100.0, 2)


def is_improvement(delta_pct: float | None, direction: str) -> str:
    """Returns 'win', 'loss', or 'noise' using the 5% timing noise floor."""
    if delta_pct is None or abs(delta_pct) < NOISE_FLOOR_PCT:
        return "noise"
    if direction == "lower_is_better":
        return "win" if delta_pct < 0 else "loss"
    return "win" if delta_pct > 0 else "loss"


def evaluate_lexicographic(
    tasks: list[dict[str, Any]],
    champion: dict[str, Any] | None,
    human_data_ok: bool,
    human_data_errors: list[str],
    mode: str = "challenger",
) -> tuple[dict[str, Any], str, str, list[dict[str, Any]]]:
    champ_by_id: dict[str, dict[str, Any]] = {}
    if champion:
        for ct in champion.get("tasks", []):
            champ_by_id[ct["id"]] = ct

    human_passed = human_total = human_regressions = 0
    human_wins = human_losses = 0
    synth_passed = synth_total = synth_regressions = 0

    enriched_tasks: list[dict[str, Any]] = []
    cand_tokens: list[float] = []
    champ_tokens: list[float] = []

    for t in tasks:
        tid = t["id"]
        tier = t.get("tier", "synthetic")
        passed = bool(t.get("binary_pass", False))
        ct = champ_by_id.get(tid)
        champ_passed = bool(ct.get("binary_pass", False)) if ct else False
        regressed = bool(ct and champ_passed and not passed)

        direction = t.get("primary_direction", "higher_is_better")
        new_val = t.get("primary_value")
        old_val = ct.get("primary_value") if ct else None
        delta = metric_delta_pct(new_val, old_val)
        outcome = is_improvement(delta, direction) if ct else "noise"

        if tier == "human":
            human_total += 1
            if passed:
                human_passed += 1
            if regressed:
                human_regressions += 1
            if outcome == "win":
                human_wins += 1
            elif outcome == "loss":
                human_losses += 1
        else:
            synth_total += 1
            if passed:
                synth_passed += 1
            if regressed:
                synth_regressions += 1

        tok = (t.get("metrics") or {}).get("tokens")
        if isinstance(tok, (int, float)):
            cand_tokens.append(float(tok))
        if ct:
            ctok = (ct.get("metrics") or {}).get("tokens")
            if isinstance(ctok, (int, float)):
                champ_tokens.append(float(ctok))

        enriched_tasks.append(
            {
                "id": tid,
                "tier": tier,
                "binary_pass": passed,
                "primary_metric": t.get("primary_metric"),
                "primary_direction": direction,
                "primary_value": new_val,
                "champion_value": old_val,
                "delta_pct": delta,
                "metrics": t.get("metrics", {}),
            }
        )

    token_ratio: float | None = None
    if cand_tokens and champ_tokens:
        med_champ = statistics.median(champ_tokens)
        if med_champ > 0:
            token_ratio = round(statistics.median(cand_tokens) / med_champ, 3)

    champ_human_passed = sum(
        1 for ct in champ_by_id.values() if ct.get("tier") == "human" and ct.get("binary_pass")
    )
    correctness_improved = bool(champion and human_passed > champ_human_passed)
    cost_ok = token_ratio is None or token_ratio <= COST_GUARDRAIL_RATIO or correctness_improved

    tier_summary = {
        "human": {
            "passed": human_passed,
            "total": human_total,
            "regressions": human_regressions,
            "primary_metric_wins": human_wins,
            "primary_metric_losses": human_losses,
        },
        "synthetic": {
            "passed": synth_passed,
            "total": synth_total,
            "regressions": synth_regressions,
        },
        "median_token_ratio_vs_champion": token_ratio,
        "cost_guardrail_passed": cost_ok,
    }

    # Gate 1: Human-input data completeness (Invariant 6)
    if not human_data_ok:
        # Synthetic-only early pruning is allowed ONLY if a synthetic binary regression occurred
        if mode == "challenger" and champion and synth_regressions > 0 and human_total == 0:
            return (
                tier_summary,
                "prune",
                f"Early prune on synthetic-only pre-screen: {synth_regressions} synthetic binary regression(s).",
                enriched_tasks,
            )
        return (
            tier_summary,
            "data_incomplete",
            "Missing or template human-input data: " + "; ".join(human_data_errors),
            enriched_tasks,
        )

    # Initial baseline run (no champion yet)
    if champion is None:
        return (
            tier_summary,
            "baseline_recorded",
            f"Recorded initial baseline: Tier 1 human {human_passed}/{human_total}, Tier 2 synthetic {synth_passed}/{synth_total}.",
            enriched_tasks,
        )

    # Champion re-run after stack or model upgrade
    if mode == "champion-rerun":
        if human_regressions > 0 or synth_regressions > 0 or human_losses > 0:
            return (
                tier_summary,
                "rewrite",
                (
                    f"Champion regressed after upgrade: human_regressions={human_regressions}, "
                    f"synthetic_regressions={synth_regressions}, human_metric_losses={human_losses}. Suite re-opened."
                ),
                enriched_tasks,
            )
        return (
            tier_summary,
            "keep_champion",
            "Champion held on upgrade re-run with zero regressions.",
            enriched_tasks,
        )

    # Challenger lexicographic evaluation
    if human_regressions > 0 or synth_regressions > 0:
        return (
            tier_summary,
            "prune",
            f"Binary regression detected: human_regressions={human_regressions}, synthetic_regressions={synth_regressions}.",
            enriched_tasks,
        )
    if human_total == 0:
        return (
            tier_summary,
            "keep_champion",
            "Synthetic-only run passed with zero regressions; promotion requires Tier 1 human-input tasks.",
            enriched_tasks,
        )
    if human_passed < human_total:
        return (
            tier_summary,
            "prune",
            f"Failed Tier 1 human binary gate ({human_passed}/{human_total}).",
            enriched_tasks,
        )
    if not cost_ok:
        return (
            tier_summary,
            "prune",
            f"Exceeded token cost guardrail: median ratio {token_ratio} > {COST_GUARDRAIL_RATIO} without correctness gain.",
            enriched_tasks,
        )
    if correctness_improved or (human_wins > human_losses):
        return (
            tier_summary,
            "promote_champion",
            (
                f"Tier 1 human gate {human_passed}/{human_total} (0 regressions), Tier 2 synthetic 0 regressions, "
                f"human metric wins={human_wins} vs losses={human_losses}, token ratio={token_ratio}."
            ),
            enriched_tasks,
        )
    return (
        tier_summary,
        "keep_champion",
        f"No net Tier 1 improvement over champion (wins={human_wins}, losses={human_losses}, noise floor={NOISE_FLOOR_PCT}%).",
        enriched_tasks,
    )


def load_run_tasks(run_dir: Path) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for p in sorted(run_dir.glob("*.json")):
        payload = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            tasks.extend(payload)
        elif isinstance(payload, dict) and "tasks" in payload:
            tasks.extend(payload["tasks"])
        elif isinstance(payload, dict) and "id" in payload:
            tasks.append(payload)
    if not tasks:
        raise ValueError(f"No task result JSON files found in {run_dir}")
    return tasks


def run_self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        data_dir = root / "data"
        data_dir.mkdir()
        human_file = data_dir / "general-spec-01-brief.json"
        human_file.write_text(
            json.dumps(
                {
                    "_header": {
                        "source": "QA @tester",
                        "date": "2026-11-22",
                        "task_id": "general-spec-01",
                        "expected_output_note": "All conflicts surfaced",
                    },
                    "data": {},
                }
            ),
            encoding="utf-8",
        )

        base_tasks = [
            {
                "id": "general-spec-01",
                "tier": "human",
                "binary_pass": True,
                "primary_metric": "conflict_recall_pct",
                "primary_direction": "higher_is_better",
                "primary_value": 80.0,
                "metrics": {"tokens": 10000, "time_sec": 40},
            },
            {
                "id": "general-refine-04",
                "tier": "synthetic",
                "binary_pass": True,
                "primary_metric": "word_reduction_pct",
                "primary_direction": "higher_is_better",
                "primary_value": 50.0,
                "metrics": {"tokens": 8000, "time_sec": 30},
            },
        ]

        # 1. Incomplete human data -> data_incomplete
        _, v1, _, _ = evaluate_lexicographic(base_tasks, None, False, ["missing file"])
        assert v1 == "data_incomplete", f"Expected data_incomplete, got {v1}"

        # 2. Valid baseline -> baseline_recorded
        ok, errs = check_suite_human_data(data_dir, base_tasks)
        assert ok and not errs, f"Unexpected human data error: {errs}"
        _, v2, _, enriched_champ = evaluate_lexicographic(base_tasks, None, ok, errs)
        assert v2 == "baseline_recorded", f"Expected baseline_recorded, got {v2}"
        champ = {"tasks": enriched_champ}

        # 3. Challenger with Tier 1 metric win -> promote_champion
        win_tasks = json.loads(json.dumps(base_tasks))
        win_tasks[0]["primary_value"] = 95.0
        _, v3, _, _ = evaluate_lexicographic(win_tasks, champ, ok, errs)
        assert v3 == "promote_champion", f"Expected promote_champion, got {v3}"

        # 4. Challenger with binary regression -> prune
        reg_tasks = json.loads(json.dumps(base_tasks))
        reg_tasks[0]["primary_value"] = 100.0
        reg_tasks[1]["binary_pass"] = False
        _, v4, _, _ = evaluate_lexicographic(reg_tasks, champ, ok, errs)
        assert v4 == "prune", f"Expected prune on binary regression, got {v4}"

        # 5. Challenger exceeding 2.0x token cost guardrail -> prune
        cost_tasks = json.loads(json.dumps(base_tasks))
        cost_tasks[0]["primary_value"] = 95.0
        cost_tasks[0]["metrics"]["tokens"] = 30000
        cost_tasks[1]["metrics"]["tokens"] = 25000
        _, v5, _, _ = evaluate_lexicographic(cost_tasks, champ, ok, errs)
        assert v5 == "prune", f"Expected prune on cost guardrail, got {v5}"

        # 6. Champion rerun regression -> rewrite
        rerun_tasks = json.loads(json.dumps(base_tasks))
        rerun_tasks[0]["primary_value"] = 60.0
        _, v6, _, _ = evaluate_lexicographic(rerun_tasks, champ, ok, errs, mode="champion-rerun")
        assert v6 == "rewrite", f"Expected rewrite on champion regression, got {v6}"

    print("score-eval.py self-test passed (6/6 verdict branches verified).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic lexicographic eval scorer.")
    parser.add_argument("--self-test", action="store_true", help="Run built-in unit tests and exit.")
    parser.add_argument("--suite", help="Suite name (general, spark, spring, or custom).")
    parser.add_argument("--variant-id", help="Unique variant identifier.")
    parser.add_argument("--variant-file", help="Path to the prompt, instruction, or skill file under test.")
    parser.add_argument("--model-id", help="Exact LLM model ID used during generation.")
    parser.add_argument("--run-dir", help="Directory containing raw per-task JSON outputs.")
    parser.add_argument("--champion-file", help="Optional path to champion JSON record in evals/results/.")
    parser.add_argument(
        "--mode",
        choices=("challenger", "champion-rerun"),
        default="challenger",
        help="Evaluation mode.",
    )
    parser.add_argument(
        "--stack-version",
        action="append",
        default=[],
        help="Stack version key=value (repeatable, e.g. --stack-version spark=3.5.0).",
    )
    parser.add_argument("--out-dir", default="evals/results", help="Output directory for immutable JSON record.")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    required = ("suite", "variant_id", "variant_file", "model_id", "run_dir")
    missing = [f"--{k.replace('_', '-')}" for k in required if not getattr(args, k)]
    if missing:
        parser.error(f"Missing required arguments: {', '.join(missing)}")

    repo_root = Path(__file__).resolve().parent.parent
    variant_path = (repo_root / args.variant_file).resolve() if not Path(args.variant_file).is_absolute() else Path(args.variant_file)
    if not variant_path.exists():
        parser.error(f"variant_file does not exist: {variant_path}")

    tasks = load_run_tasks(Path(args.run_dir))
    champion = json.loads(Path(args.champion_file).read_text(encoding="utf-8")) if args.champion_file else None
    data_dir = repo_root / "evals" / "data" / args.suite
    human_ok, human_errs = check_suite_human_data(data_dir, tasks)

    tier_summary, verdict, reason, enriched = evaluate_lexicographic(
        tasks=tasks,
        champion=champion,
        human_data_ok=human_ok,
        human_data_errors=human_errs,
        mode=args.mode,
    )

    stack_versions: dict[str, str] = {"python": sys.version.split()[0]}
    for item in args.stack_version:
        if "=" in item:
            k, v = item.split("=", 1)
            stack_versions[k.strip()] = v.strip()

    now = dt.datetime.now(dt.timezone.utc)
    record = {
        "date": now.strftime("%Y-%m-%d"),
        "git_sha": get_git_sha(repo_root),
        "model_id": args.model_id,
        "stack_versions": stack_versions,
        "suite": args.suite,
        "variant_id": args.variant_id,
        "variant_file": args.variant_file,
        "prompt_hash": sha256_file(variant_path),
        "champion_id": champion.get("variant_id") if champion else None,
        "human_data_status": "complete" if human_ok else "incomplete",
        "tier_summary": tier_summary,
        "tasks": enriched,
        "verdict": verdict,
        "verdict_reason": reason,
    }

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = now.strftime("%Y%m%d-%H%M%S")
    out_file = out_dir / f"{args.suite}-{args.variant_id}-{ts}.json"
    out_file.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_file} | verdict={verdict} | {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
