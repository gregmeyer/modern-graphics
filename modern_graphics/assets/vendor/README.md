# Vendored JavaScript

These files are bundled so chart layouts render offline (Playwright loads HTML via `file://`).

- `chart.umd.min.js` — Chart.js v4.4.7 (MIT) — https://www.chartjs.org/
- `chartjs-chart-sankey.min.js` — chartjs-chart-sankey v0.12.1 (MIT) — https://github.com/kurkle/chartjs-chart-sankey

## Update

```sh
curl -sSL -o chart.umd.min.js "https://cdn.jsdelivr.net/npm/chart.js@<version>/dist/chart.umd.min.js"
curl -sSL -o chartjs-chart-sankey.min.js "https://cdn.jsdelivr.net/npm/chartjs-chart-sankey@<version>/dist/chartjs-chart-sankey.min.js"
```
