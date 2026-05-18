# model-efficiency-evaluation-pipeline

An automated CI/CD pipeline that treats LLM accuracy, latency and API costs as breaking test failures, enforcing the maintainability and efficiency of AI-powered features.

## How it works

This repository includes a CI workflow (`.github/workflows/model-efficiency-gate.yml`) that:

- runs unit tests for the metric gate logic;
- evaluates measured model metrics from `ci/latest_metrics.json`;
- fails the build when metrics violate limits in `ci/thresholds.json`.

## Local validation

```bash
python -m unittest discover -s tests -p "test_*.py"
python ci/evaluate_metrics.py --thresholds ci/thresholds.json --metrics ci/latest_metrics.json
```

Update `ci/latest_metrics.json` with your measured values in your own pipeline so pull requests fail on regressions in accuracy, latency, or API cost.
