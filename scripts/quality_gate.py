#!/usr/bin/env python3
"""Check essential distribution artifacts and local link targets."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
needed = [
    "README.md", "README.zh.md", "LICENSE", "AGENTS.md", "CLAUDE.md",
    ".github/workflows/ci.yml", ".claude-plugin/plugin.json",
    "skills/five-step-optimizer/SKILL.md",
    "skills/five-step-optimizer/scripts/process_metrics.py",
    "skills/five-step-optimizer/scripts/validate_case.py",
    "skills/five-step-optimizer/scripts/render_flow.py",
    "examples/gigacasting-synthetic.json", "examples/software-bugflow-synthetic.json",
    "templates/decision-record.md", "templates/intake.md",
]
problems = [f"Missing: {p}" for p in needed if not (ROOT / p).is_file()]
skill = (ROOT / "skills/five-step-optimizer/SKILL.md").read_text(encoding="utf-8")
if not skill.startswith("---\n") or "name: five-step-optimizer" not in skill or "description:" not in skill:
    problems.append("Invalid SKILL.md frontmatter")
for ref in re.findall(r"`(references/[^\s`]+\.md)`", skill):
    if not (ROOT / "skills/five-step-optimizer" / ref).is_file():
        problems.append("Broken skill reference: " + ref)
if problems:
    print("\n".join(problems))
    sys.exit(1)
print("PASS: required project distribution and references")
