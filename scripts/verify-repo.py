#!/usr/bin/env python3
"""Mechanical acceptance verifier for the repository (SPEC.md Sections 7 & 9).

Checks:
1. English-only prose across all added layers (zero CJK characters).
2. Zero em-dashes in added layers (per CLAUDE.md).
3. Zero leaderboard, Elo, arena, or win-rate language in added layers.
4. Byte-identical canonical Selection, Pruning, and Contingency block across
   copilot-instructions.md, gardener-mode.agent.md, spark-spring-mode.agent.md,
   and evals/README.md.
5. Every eval suite (general, spark, spring) has 6 tasks, all 5 required fields,
   and 'Baseline: to be measured' until replaced by real runs.
6. Valid frontmatter on all added .github/instructions, .github/agents, and
   .github/prompts files.
7. evals/results/ contains only valid JSON records or explicitly marked examples.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ADDED_FILES_GLOBS = [
    ".github/copilot-instructions.md",
    ".github/instructions/*.md",
    ".github/agents/*.md",
    ".github/prompts/*.md",
    "evals/**/*.md",
    "evals/**/*.json",
    "scripts/score-eval.py",
    "scripts/verify-repo.py",
    "SPEC.md",
    "ADAPTATION.md",
    "docs/methodology.md",
]

CANONICAL_FILES = [
    ".github/copilot-instructions.md",
    ".github/agents/gardener-mode.agent.md",
    ".github/agents/spark-spring-mode.agent.md",
    "evals/README.md",
]

BEGIN_MARK = "<!-- BEGIN CANONICAL SELECTION AND CONTINGENCY RULES -->"
END_MARK = "<!-- END CANONICAL SELECTION AND CONTINGENCY RULES -->"

FORBIDDEN_ARENA_RE = re.compile(r"\b(leaderboard|elo|win[\s-]?rate|arena)\b", re.IGNORECASE)
CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def iter_added_files() -> list[Path]:
    seen: set[Path] = set()
    files: list[Path] = []
    for pattern in ADDED_FILES_GLOBS:
        for p in sorted(ROOT.glob(pattern)):
            if p.is_file() and p not in seen:
                seen.add(p)
                files.append(p)
    return files


def extract_canonical(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    start = text.find(BEGIN_MARK)
    end = text.find(END_MARK)
    if start == -1 or end == -1 or end <= start:
        return None
    return text[start : end + len(END_MARK)].strip()


def main() -> int:
    errors: list[str] = []
    added_files = iter_added_files()

    # 1, 2, 3: English-only, no em-dashes, no arena/leaderboard/Elo language
    for path in added_files:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        if CJK_RE.search(text):
            errors.append(f"[Invariant 7] Non-English CJK characters found in {rel}")
        if "\u2014" in text:
            errors.append(f"[Style] Em-dash found in {rel}")
        # Skip self-reference regex in verify-repo.py
        if rel != "scripts/verify-repo.py":
            for m in FORBIDDEN_ARENA_RE.finditer(text):
                errors.append(f"[Check 9.6] Forbidden ranking/arena term '{m.group(0)}' in {rel}")

    # 4: Identical canonical Selection, Pruning, and Contingency block
    blocks: dict[str, str] = {}
    for rel in CANONICAL_FILES:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"[Check 9.5] Missing required file: {rel}")
            continue
        blk = extract_canonical(p)
        if blk is None:
            errors.append(f"[Check 9.5] Missing canonical rules markers in {rel}")
        else:
            blocks[rel] = blk
    if blocks:
        ref_file, ref_block = next(iter(blocks.items()))
        for rel, blk in blocks.items():
            if blk != ref_block:
                errors.append(f"[Check 9.5] Canonical rules block in {rel} differs from {ref_file}")

    # 5: Eval suites (general, spark, spring) have 6 tasks and all 5 fields
    for suite in ("general", "spark", "spring"):
        tpath = ROOT / "evals" / suite / "tasks.md"
        if not tpath.exists():
            errors.append(f"[Check 9.3] Missing suite file: evals/{suite}/tasks.md")
            continue
        text = tpath.read_text(encoding="utf-8")
        task_sections = re.split(r"(?m)^## Task \d+:", text)[1:]
        if len(task_sections) != 6:
            errors.append(f"[Check 9.3] evals/{suite}/tasks.md has {len(task_sections)} tasks (expected 6)")
        for idx, sec in enumerate(task_sections, 1):
            for field in ("**Input**", "**Operation**", "**Scoring**", "**Baseline:**", "**Human-Input Data:**"):
                if field not in sec:
                    errors.append(f"[Check 9.3] evals/{suite}/tasks.md Task {idx} missing {field}")
            if "**Baseline:** to be measured" not in sec:
                errors.append(f"[Check 9.3] evals/{suite}/tasks.md Task {idx} baseline is not 'to be measured'")

    # 6: YAML frontmatter presence on .github/instructions, agents, prompts
    for folder in (".github/instructions", ".github/agents", ".github/prompts"):
        for p in sorted((ROOT / folder).glob("*.md")):
            text = p.read_text(encoding="utf-8")
            if not re.match(r"^---\r?\n[\s\S]*?\r?\n---", text):
                errors.append(f"[Frontmatter] Missing YAML frontmatter in {p.relative_to(ROOT).as_posix()}")

    # 7: evals/results/ JSON records schema check
    results_dir = ROOT / "evals" / "results"
    for p in sorted(results_dir.glob("*.json")):
        try:
            rec = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"[Check 9.4] Invalid JSON in {p.name}: {exc}")
            continue
        req_keys = ("date", "git_sha", "model_id", "stack_versions", "variant_id", "tasks", "verdict")
        for k in req_keys:
            if k not in rec:
                errors.append(f"[Check 9.4] Missing key '{k}' in {p.name}")
        if "total_score" in rec:
            errors.append(f"[Check 9.4] Forbidden blended 'total_score' found in {p.name}")

    if errors:
        print("Repository verification FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"Repository verification PASSED ({len(added_files)} added files checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
