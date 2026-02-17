# Strategy Extension Contract

This guide defines the minimum bar for adding a new layout strategy.

## Required Artifacts

1. **Payload model**
- Add a typed payload model in `modern_graphics/layout_models.py`.
- Validate required fields in `__post_init__`.
- Provide `to_strategy_kwargs()` for renderer compatibility.

2. **Strategy registration**
- Register strategy in `modern_graphics/layouts.py` with:
  - unique `layout_type`
  - explicit `required_args`
  - renderer function with deterministic output.

3. **Smoke fixture**
- Add at least one fixture under `tests/smoke/`.
- Ensure smoke test renders the strategy via `generate_layout`.

4. **Quality gate expectations**
- Ensure fixture metrics can be evaluated by `run_clarity_gates`.
- If strategy is insight-oriented, include:
  - headline hierarchy
  - panel density
  - panel balance
  - whitespace bounds

5. **Docs update**
- Update `README.md` layout list if user-facing.
- Update `docs/OVERHAUL_SPEC.md` checkpoint notes.

## Extension Flow

1. Define payload model.
2. Implement renderer.
3. Register strategy.
4. Add smoke fixture.
5. Run:
   - `python scripts/validate_overhaul_phase1.py`
   - `python scripts/run_phase1_quality_harness.py`
   - `python scripts/run_insight_fixture_harness.py` (for insight-style layouts)

## Reference Example

- See `modern_graphics/strategy_examples.py`:
  - `CalloutPayload`
  - `register_example_callout_strategy()`

