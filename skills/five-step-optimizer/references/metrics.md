# Metrics and model limits

All quantities require units, scope and data provenance. Distinguish ideal capacity, measured throughput, availability, yield, OEE, lead time and cycle time.

For a serial single-product flow **without rework, buffers, blocking, starvation or shared resources**:
- At stage i, raw attempts/hour = `3600 / cycle_seconds_i * machines_i * availability_i`.
- Output-good capacity at the final stage (upper bound) = `min_i(raw_attempts_i * product(yield_j for j from i to n))`.
- Expected variable cost per first-pass-good output = `sum_i(variable_cost_per_attempt_i / product(yield_j for j from i to n))`.

Assume independent stage yields and that scrap exits at the stage detecting it. Costs are per stage attempt (including attempts later scrapped); this model ignores salvage and rework. If throughput demand or buffers conflict, model additional constraints instead of promising output.

Economics: `annual_net_operating_benefit = annual_good_units * (before_unit_variable_cost - after_unit_variable_cost) - incremental_annual_fixed_cost`. When benefit is positive, `simple_payback_years = incremental_capex / annual_net_operating_benefit`. This is not NPV/IRR or TCO. Include lifecycle maintenance, tooling, energy, capex, ramp-up, downtime, warranty and salvage separately when making a real decision.

Use uncertainty ranges and sensitivity analysis for capex, demand, availability and yield. Never treat hypothetical manufacturing metrics as reported Tesla performance.
