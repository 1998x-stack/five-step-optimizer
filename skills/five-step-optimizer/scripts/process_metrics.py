#!/usr/bin/env python3
"""Serial no-rework independent-yield capacity/cost UPPER BOUND; not a digital twin."""
import argparse
import json
import math
from pathlib import Path
from validate_case import validate


def analyze_line(line):
    steps = line["steps"]
    downstream_yield = 1.0
    rows = []
    for step in reversed(steps):
        cycle = float(step["cycle_seconds"])
        machines = int(step["machines"])
        available = float(step["availability"])
        good = float(step["yield"])
        variable_cost = float(step["variable_cost_per_attempt"])
        downstream_yield *= good
        capacity = 3600 / cycle * machines * available
        rows.append({
            "id": step["id"], "name": step["name"],
            "final_good_capacity_per_hour": capacity * downstream_yield,
            "cost_per_final_good": variable_cost / downstream_yield,
        })
    rows.reverse()
    bottleneck = min(rows, key=lambda x: x["final_good_capacity_per_hour"])
    return {
        "line": line["name"],
        "bottleneck_step": bottleneck["id"],
        "good_units_per_hour_upper_bound": bottleneck["final_good_capacity_per_hour"],
        "line_first_pass_yield": downstream_yield,
        "variable_cost_per_good": sum(x["cost_per_final_good"] for x in rows),
        "steps": rows,
        "limitation": "Simplified serial flow, independent stage yields, no blocking, buffers, shared resources or rework.",
    }


def analyze_case(case):
    problems = validate(case)
    if problems:
        raise ValueError("Invalid case: " + "; ".join(problems))
    before = analyze_line(case["baseline"])
    after = analyze_line(case["proposed"])
    out = {"case_id": case["case_id"], "classification": case["data_classification"],
           "baseline": before, "proposed": after}
    if "economics" in case:
        e = case["economics"]
        units = float(e["annual_good_units"])
        annual_fixed = float(e["incremental_annual_fixed_cost"])
        capex = float(e["incremental_capex"])
        saving = before["variable_cost_per_good"] - after["variable_cost_per_good"]
        annual = units * saving - annual_fixed
        out["economics"] = {
            "currency": e.get("currency", "unspecified"),
            "unit_variable_cost_saving": saving,
            "annual_net_operating_benefit": annual,
            "simple_payback_years": capex / annual if annual > 0 else None,
            "limitation": "Illustrative simple payback, not NPV/IRR/TCO or proof of physical deliverability.",
        }
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("case", type=Path)
    p.add_argument("--out", type=Path)
    a = p.parse_args()
    output = json.dumps(analyze_case(json.loads(a.case.read_text(encoding="utf-8"))), ensure_ascii=False, indent=2)
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
