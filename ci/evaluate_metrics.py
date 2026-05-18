#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path


def _load_json(file_path: Path) -> dict:
    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"{file_path} must contain a JSON object.")
    return data


def evaluate(metrics: dict, thresholds: dict) -> list[str]:
    errors: list[str] = []

    for metric_name, rules in thresholds.items():
        if metric_name not in metrics:
            errors.append(f"Missing metric: {metric_name}")
            continue

        value = metrics[metric_name]
        if not isinstance(value, (int, float)):
            errors.append(f"Metric '{metric_name}' must be numeric, got {type(value).__name__}.")
            continue

        if "min" in rules and value < rules["min"]:
            errors.append(
                f"{metric_name} below minimum: {value} < {rules['min']}"
            )

        if "max" in rules and value > rules["max"]:
            errors.append(
                f"{metric_name} above maximum: {value} > {rules['max']}"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail CI when LLM accuracy, latency, or cost regress beyond thresholds."
    )
    parser.add_argument(
        "--metrics",
        default="ci/latest_metrics.json",
        help="Path to JSON file with measured metrics.",
    )
    parser.add_argument(
        "--thresholds",
        default="ci/thresholds.json",
        help="Path to JSON file with pass/fail thresholds.",
    )
    args = parser.parse_args()

    metrics_path = Path(args.metrics)
    thresholds_path = Path(args.thresholds)

    if not metrics_path.exists():
        print(f"Metrics file not found: {metrics_path}")
        return 1

    if not thresholds_path.exists():
        print(f"Thresholds file not found: {thresholds_path}")
        return 1

    try:
        metrics = _load_json(metrics_path)
        thresholds = _load_json(thresholds_path)
        violations = evaluate(metrics, thresholds)
    except (json.JSONDecodeError, ValueError) as error:
        print(f"Configuration error: {error}")
        return 1

    if violations:
        print("Model efficiency gate failed:")
        for violation in violations:
            print(f"- {violation}")
            
        summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary_file:
            with open(summary_file, "a", encoding="utf-8") as f:
                f.write("## ❌ Model Efficiency Gate Failed\n\n")
                f.write("| Metric | Value |\n|---|---|\n")
                for m, v in metrics.items():
                    f.write(f"| {m} | {v} |\n")
                f.write("\n**Violations:**\n")
                for v in violations:
                    f.write(f"- {v}\n")
                    
        return 1

    print("Model efficiency gate passed.")
    
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write("## ✅ Model Efficiency Gate Passed\n\n")
            f.write("| Metric | Value |\n|---|---|\n")
            for m, v in metrics.items():
                f.write(f"| {m} | {v} |\n")
                
    return 0


if __name__ == "__main__":
    sys.exit(main())
