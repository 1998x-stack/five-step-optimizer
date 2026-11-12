#!/usr/bin/env python3
"""Install the canonical skill into the selected project's agent skill directory."""
import argparse
import shutil
from pathlib import Path

TARGETS = {
    "codex": ".codex/skills",
    "claude": ".claude/skills",
    "pi": ".pi/skills",
    "opencode": ".opencode/skills",
    "cursor": ".cursor/skills",
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--target", required=True, choices=TARGETS)
    p.add_argument("--base", type=Path, default=Path.cwd())
    p.add_argument("--overwrite", action="store_true")
    args = p.parse_args()
    src = Path(__file__).resolve().parents[1] / "skills" / "five-step-optimizer"
    dst = args.base.resolve() / TARGETS[args.target] / "five-step-optimizer"
    if dst.exists() and not args.overwrite:
        p.error("Destination exists; use --overwrite if you intend to replace: " + str(dst))
    if dst.exists():
        if not dst.is_dir():
            p.error("Target exists but is not a directory: " + str(dst))
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)
    print("Installed:", dst)


if __name__ == "__main__":
    main()
