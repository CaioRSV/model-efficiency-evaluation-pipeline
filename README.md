# model-efficiency-evaluation-pipeline

An automated CI/CD pipeline that treats LLM accuracy, latency and API costs as breaking test failures, enforcing the maintainability and efficiency of AI-powered features.

## How it works

This repository includes a CI workflow (`.github/workflows/model-efficiency-gate.yml`) that:

- Runs unit tests for the metric gate logic.
- Dynamically evaluates a local LLM (`qwen:0.5b` via Ollama) using `ci/run_evaluation.py`.
- Generates `ci/latest_metrics.json` at runtime.
- Fails the build when measured metrics violate the limits defined in `ci/thresholds.json`.
- Publishes a beautifully formatted Markdown table of the results directly to the Pull Request's GitHub Step Summary.

## Local validation

To run the model evaluation locally, make sure you have [Ollama](https://ollama.com/) installed and running:
```bash
ollama pull qwen:0.5b
ollama serve
```

Then, run the evaluation script to dynamically generate `ci/latest_metrics.json`:
```bash
python ci/run_evaluation.py
```

Check the generated metrics against your thresholds:
```bash
python -m unittest discover -s tests -p "test_*.py"
python ci/evaluate_metrics.py --thresholds ci/thresholds.json --metrics ci/latest_metrics.json
```

The pipeline is set up to automatically block pull requests on regressions in accuracy, latency, or API cost based on live model evaluation!
