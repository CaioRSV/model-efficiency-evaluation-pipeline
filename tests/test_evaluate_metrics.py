import unittest

from ci.evaluate_metrics import evaluate


class EvaluateMetricsTests(unittest.TestCase):
    def setUp(self):
        self.thresholds = {
            "accuracy": {"min": 0.85},
            "latency_ms": {"max": 1200},
            "cost_usd": {"max": 0.02},
        }

    def test_passes_within_thresholds(self):
        metrics = {"accuracy": 0.9, "latency_ms": 900, "cost_usd": 0.01}
        self.assertEqual(evaluate(metrics, self.thresholds), [])

    def test_fails_when_accuracy_is_below_minimum(self):
        metrics = {"accuracy": 0.8, "latency_ms": 900, "cost_usd": 0.01}
        errors = evaluate(metrics, self.thresholds)
        self.assertIn("accuracy below minimum: 0.8 < 0.85", errors)

    def test_fails_when_latency_is_above_maximum(self):
        metrics = {"accuracy": 0.9, "latency_ms": 1400, "cost_usd": 0.01}
        errors = evaluate(metrics, self.thresholds)
        self.assertIn("latency_ms above maximum: 1400 > 1200", errors)

    def test_fails_when_cost_is_above_maximum(self):
        metrics = {"accuracy": 0.9, "latency_ms": 900, "cost_usd": 0.04}
        errors = evaluate(metrics, self.thresholds)
        self.assertIn("cost_usd above maximum: 0.04 > 0.02", errors)

    def test_fails_when_metric_is_missing(self):
        metrics = {"accuracy": 0.9, "latency_ms": 900}
        errors = evaluate(metrics, self.thresholds)
        self.assertIn("Missing metric: cost_usd", errors)


if __name__ == "__main__":
    unittest.main()
