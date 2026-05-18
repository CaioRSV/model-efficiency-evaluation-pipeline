import json
import time
import urllib.request
import urllib.error
from pathlib import Path

def evaluate_ollama():
    # A simple dataset to test the model
    dataset = [
        {"prompt": "Answer with only the number. What is 2 + 2?", "expected": "4"},
        {"prompt": "Answer with only the name of the city. What is the capital of France?", "expected": "paris"},
        {"prompt": "Answer with only the word. The opposite of 'hot' is?", "expected": "cold"}
    ]
    
    correct_predictions = 0
    total_latency_ms = 0
    
    url = "http://localhost:11434/api/generate"
    model_name = "qwen:0.5b" # Extremely fast and small model for CI (less than 400mb)
    
    for item in dataset:
        payload = {
            "model": model_name,
            "prompt": item["prompt"],
            "stream": False
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        start_time = time.time()
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                prediction = result.get("response", "").strip().lower()
                print(f"Prompt: {item['prompt']}")
                print(f"Prediction: {prediction}")
        except urllib.error.URLError as e:
            print(f"Error querying Ollama: {e}")
            prediction = ""
            
        latency_ms = (time.time() - start_time) * 1000
        total_latency_ms += latency_ms
        
        if item["expected"] in prediction:
            correct_predictions += 1
            
    num_items = len(dataset)
    metrics = {
        "accuracy": round(correct_predictions / num_items, 2) if num_items > 0 else 0,
        "latency_ms": round(total_latency_ms / num_items, 2) if num_items > 0 else 0,
        "cost_usd": 0.0 # Local ollama is free
    }

    # Dump the metrics dynamically to the JSON file
    metrics_path = Path("ci/latest_metrics.json")
    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    print(f"Generated metrics: {metrics}")

if __name__ == "__main__":
    evaluate_ollama()
