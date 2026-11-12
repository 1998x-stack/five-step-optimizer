#!/usr/bin/env python3
"""Render static SVG only; user data are XML-escaped."""
import argparse
import json
from pathlib import Path
from xml.sax.saxutils import escape
from validate_case import validate


def render(case):
    problems = validate(case)
    if problems:
        raise ValueError("Invalid case: " + "; ".join(problems))
    before, after = case["baseline"]["steps"], case["proposed"]["steps"]
    height = 125 + 70 * max(len(before), len(after))
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" viewBox="0 0 900 {height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#1e293b}.head{font-size:20px;font-weight:bold}.item{font-size:14px}.detail{font-size:11px;fill:#475569}</style>',
        '<text class="head" x="30" y="35">BEFORE</text><text class="head" x="480" y="35">AFTER</text>',
    ]
    for column, steps in enumerate((before, after)):
        x = 30 + column * 450
        for i, step in enumerate(steps):
            y = 55 + 70 * i
            name = escape(step["name"][:44])
            out.append(f'<rect x="{x}" y="{y}" width="390" height="51" rx="8" fill="#e2e8f0" stroke="#64748b"/>')
            out.append(f'<text class="item" x="{x+12}" y="{y+22}">{name}</text>')
            out.append(f'<text class="detail" x="{x+12}" y="{y+41}">cycle {step["cycle_seconds"]:g}s · machines {step["machines"]} · yield {100*step["yield"]:.1f}%</text>')
            if i < len(steps) - 1:
                out.append(f'<path d="M{x+195} {y+51}v16" stroke="#475569" stroke-width="2"/>')
    out.append(f'<text class="detail" x="30" y="{height-17}">{escape(case["data_classification"])} example; not an engineering drawing.</text>')
    out.append('</svg>')
    return "\n".join(out) + "\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("case", type=Path)
    p.add_argument("output", type=Path)
    a = p.parse_args()
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(render(json.loads(a.case.read_text(encoding="utf-8"))), encoding="utf-8")
    print("Wrote", a.output)


if __name__ == "__main__":
    main()
