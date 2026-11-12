---
name: five-step-optimizer
description: Evidence-driven redesign of manufacturing, software and business workflows using Question Requirements, Delete, Simplify, Accelerate, Automate. Use when investigating unnecessary process steps, throughput, bottlenecks, quality, economics or automation. Require explicit safety gates and verifiable acceptance criteria.
license: MIT
---

# Five-Step Optimizer

**Mission:** Maximize verified end-to-end value using the least necessary work, not the most automation.

The five steps are **Question requirements → Delete → Simplify / optimize → Accelerate → Automate**, always in that order. Evidence intake and verification surround the steps. This skill advises; it does not authorize changes to production or safety-critical systems.

## Route

Read only the references needed:
- Manufacturing: `references/manufacturing-playbook.md` and `references/metrics.md`
- Software: `references/software-playbook.md`
- Evidence uncertain: `references/evidence-standards.md`
- Physical safety, quality, legal or security risks: `references/safety-quality-gates.md`
- Teaching example: `references/case-study-gigacasting.md`

## Gate 0: evidence and requirements

Define process boundary, unit of output, demand, baseline period, customer value, target, owner and constraints. Map actual steps before proposing modifications. Tag every number as **observed**, **documented**, **assumed** or **unknown** with source, dates and units.

Identify non-negotiable safety, regulatory, inspection, security and environmental controls. **Unknown is not permission to delete.** If real plant data are missing, use explicit hypotheticals and request the necessary measurements. Never fabricate observed ROI or real-company metrics.

## The algorithm

1. **Question Requirements:** For every rule, ask who owns it, why it exists, the protected function, evidence, current relevance and failure mode if removed. Unowned is a research task, not an automatic delete.
2. **Delete:** Identify non-value-adding operations, parts, approvals and transfers. For each deletion candidate record protected function, potential adverse effects, alternate controls, owner, evidence and reversible test. Mandatory controls must be retained unless the proper authority approves an equivalent compliant control.
3. **Simplify / Optimize:** Reduce components, interfaces, handoffs and variation in the remaining system. Compare alternatives; prefer the smallest viable redesign rather than speculative complexity.
4. **Accelerate:** Find the *end-to-end, quality-adjusted* bottleneck, not the fastest individual machine. Evaluate availability, changeover, first-pass yield, rework, inspection, maintenance, WIP and upstream/downstream coupling. Do not sacrifice safety or downstream quality to improve local cycle time.
5. **Automate:** Automate only a stable, demonstrated process with documented sensors, monitoring, safe failure, interlocks, human oversight, cybersecurity, change control and rollback. An AI recommendation is not permission to actuate machinery.

## Decision & acceptance

For each proposed change provide: baseline and source; after-state hypothesis; measurable predicted benefit **and** downside; costs and assumptions; protected constraints; test owner; acceptance/stop thresholds; and rollback. Prefer bounded experiments over confident unverified claims.

Use `templates/decision-record.md` and `templates/intake.md` when appropriate. For a JSON case run:
```bash
python skills/five-step-optimizer/scripts/validate_case.py examples/gigacasting-synthetic.json
python skills/five-step-optimizer/scripts/process_metrics.py examples/gigacasting-synthetic.json
python skills/five-step-optimizer/scripts/render_flow.py examples/gigacasting-synthetic.json /tmp/flow.svg
```

The calculator is a simplified serial, no-rework, independent-yield, upper-bound model. It is not a validated digital twin. A **recommendation** is never an approved plant change.

## Required output

A concise executive decision followed by (1) scope and evidence ledger; (2) before/after process flow; (3) questioned requirements and deletion register; (4) feasible alternatives; (5) bottleneck/quality/cost with uncertainty; (6) safety gates; (7) controlled pilot, roles, checks and rollback; (8) explicit **proposed / blocked / trial-validated / authorized-by-owner** status. State what is *not* known.
