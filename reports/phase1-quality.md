# Phase 1 Quality Report

- pass: **2**
- warn: **2**
- fail: **4**

## Per Layout

### hero - PASS
- `min_text_size`: **pass** - OK
- `focal_point_budget`: **pass** - OK
- `density_budget`: **pass** - OK
- `contrast_ratio`: **pass** - OK
- `whitespace_guard`: **pass** - OK

### insight-card - PASS
- `min_text_size`: **pass** - OK
- `focal_point_budget`: **pass** - OK
- `density_budget`: **pass** - OK
- `contrast_ratio`: **pass** - OK
- `whitespace_guard`: **pass** - OK

### story-slide - WARN
- soft warns: `density_budget, focal_point_budget`
- `min_text_size`: **pass** - OK
- `focal_point_budget`: **warn** - Observed 3 focal points above target 2
- `density_budget`: **warn** - Density items 10 above target 8
- `contrast_ratio`: **pass** - OK
- `whitespace_guard`: **pass** - OK

### comparison - FAIL
- hard fails: `min_text_size`
- `min_text_size`: **fail** - Observed 12px below minimum 13px
- `focal_point_budget`: **pass** - OK
- `density_budget`: **pass** - OK
- `contrast_ratio`: **pass** - OK
- `whitespace_guard`: **pass** - OK

### timeline - FAIL
- hard fails: `contrast_ratio, min_text_size`
- soft warns: `density_budget, focal_point_budget`
- `min_text_size`: **fail** - Observed 11px below minimum 13px
- `focal_point_budget`: **warn** - Observed 3 focal points above target 2
- `density_budget`: **warn** - Density items 9 above target 8
- `contrast_ratio`: **fail** - Contrast ratio 4.20 below minimum 4.50
- `whitespace_guard`: **pass** - OK

### funnel - FAIL
- hard fails: `whitespace_guard, min_text_size`
- `min_text_size`: **fail** - Observed 12px below minimum 13px
- `focal_point_budget`: **pass** - OK
- `density_budget`: **pass** - OK
- `contrast_ratio`: **pass** - OK
- `whitespace_guard`: **fail** - Whitespace ratio 0.37 above maximum 0.35

### grid - WARN
- soft warns: `density_budget, focal_point_budget`
- `min_text_size`: **pass** - OK
- `focal_point_budget`: **warn** - Observed 4 focal points above target 2
- `density_budget`: **warn** - Density items 11 above target 8
- `contrast_ratio`: **pass** - OK
- `whitespace_guard`: **pass** - OK

### pyramid - FAIL
- hard fails: `min_text_size`
- `min_text_size`: **fail** - Observed 12px below minimum 13px
- `focal_point_budget`: **pass** - OK
- `density_budget`: **pass** - OK
- `contrast_ratio`: **pass** - OK
- `whitespace_guard`: **pass** - OK
