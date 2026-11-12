#!/usr/bin/env python3
"""Structural/units validation, not engineering certification."""
import argparse
import json
import math
from pathlib import Path

CLASSIFICATIONS = {"synthetic", "observed", "documented", "mixed"}
DECISIONS = {"retain", "challenge", "delete", "remove", "simplify", "verify"}
FIELDS = ("cycle_seconds", "machines", "availability", "yield", "variable_cost_per_attempt")


def number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    result = float(value)
    return result if math.isfinite(result) else None


def validate(case):
    errors = []
    if not isinstance(case, dict):
        return ["Case must be a JSON object"]
    for key in ("case_id", "scope"):
        if not isinstance(case.get(key), str) or not case[key].strip():
            errors.append("Missing or invalid " + key)
    if not isinstance(case.get("data_classification"), str) or case["data_classification"] not in CLASSIFICATIONS:
        errors.append("Unrecognized data classification")
    for key in ("protected_constraints", "evidence"):
        if not isinstance(case.get(key), list) or not case[key]:
            errors.append(key + " must be a nonempty list")
    for i, item in enumerate(case.get("protected_constraints", []) if isinstance(case.get("protected_constraints"), list) else []):
        if not isinstance(item, str) or not item.strip():
            errors.append("Invalid protected constraint " + str(i))
    requirements = case.get("requirements")
    if not isinstance(requirements, list):
        errors.append("requirements must be a list")
        requirements = []
    seen = set()
    for i, req in enumerate(requirements):
        if not isinstance(req, dict):
            errors.append("Requirement must be an object: " + str(i))
            continue
        for key in ("id", "owner", "requirement", "mandatory", "decision", "source"):
            if key not in req or req[key] in (None, ""):
                errors.append("Requirement missing " + key + ": " + str(i))
        ident = req.get("id")
        if not isinstance(ident, str) or not ident.strip():
            errors.append("Invalid requirement ID: " + str(i))
        elif ident in seen:
            errors.append("Duplicate requirement ID: " + ident)
        else:
            seen.add(ident)
        if type(req.get("mandatory")) is not bool:
            errors.append("mandatory must be boolean: " + str(ident))
        if req.get("decision") not in DECISIONS if isinstance(req.get("decision"), str) else True:
            errors.append("Unknown decision: " + str(ident))
        if req.get("mandatory") is True and req.get("decision") in ("delete", "remove"):
            errors.append("Cannot delete mandatory requirement: " + str(ident))
    evidence = case.get("evidence")
    if isinstance(evidence, list):
        for i, item in enumerate(evidence):
            if not isinstance(item, dict) or not all(isinstance(item.get(k), str) and item[k].strip() for k in ("claim", "source", "classification")):
                errors.append("Evidence missing claim/source/classification: " + str(i))
            elif case.get("data_classification") == "synthetic" and item["classification"] not in ("synthetic", "assumed"):
                errors.append("Synthetic case mislabels evidence: " + str(i))
    for scenario in ("baseline", "proposed"):
        line = case.get(scenario)
        if not isinstance(line, dict) or not isinstance(line.get("steps"), list) or not line["steps"]:
            errors.append(scenario + " must have a nonempty steps list")
            continue
        if not isinstance(line.get("name"), str) or not line["name"].strip():
            errors.append(scenario + " missing line name")
        seen_steps = set()
        for i, step in enumerate(line["steps"]):
            if not isinstance(step, dict):
                errors.append(scenario + " step is not an object: " + str(i))
                continue
            sid = step.get("id")
            if not isinstance(sid, str) or not sid.strip() or sid in seen_steps:
                errors.append(scenario + " missing/duplicate step ID: " + str(i))
            else:
                seen_steps.add(sid)
            if not isinstance(step.get("name"), str) or not step["name"].strip():
                errors.append(scenario + " missing step name: " + str(i))
            for field in FIELDS:
                value = number(step.get(field))
                ok = value is not None
                if field in ("cycle_seconds", "machines"):
                    ok = ok and value > 0
                if field in ("availability", "yield"):
                    ok = ok and 0 < value <= 1
                if field == "variable_cost_per_attempt":
                    ok = ok and value >= 0
                if field == "machines":
                    ok = ok and value.is_integer()
                if not ok:
                    errors.append(scenario + " invalid " + field + " at step " + str(i))
    if "economics" in case:
        e = case["economics"]
        if not isinstance(e, dict):
            errors.append("economics must be an object")
        else:
            for key in ("annual_good_units", "incremental_annual_fixed_cost", "incremental_capex"):
                value = number(e.get(key))
                if value is None or value < 0:
                    errors.append("Invalid economics " + key)
    return errors


def main():
    p = argparse.ArgumentParser()
    p.add_argument("case", type=Path)
    args = p.parse_args()
    problems = validate(json.loads(args.case.read_text(encoding="utf-8")))
    if problems:
        print("FAIL\n" + "\n".join(problems))
        raise SystemExit(1)
    print("PASS: input bounds and evidence classification (not engineering approval)")


if __name__ == "__main__":
    main()
