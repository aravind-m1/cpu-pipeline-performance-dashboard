from flask import Flask, render_template, jsonify
import random
from collections import deque
import os

app = Flask(__name__)

# Simulated pipeline data
pipeline_stages = ["Fetch", "Decode", "Execute", "Memory", "Writeback"]
pipeline_utilization = {stage: 0 for stage in pipeline_stages}
performance_metrics = {
    "CPI": 1.0,
    "IPC": 1.0,
    "Stalls": 0,
    "BranchMispredict": 0,
    "CacheMisses": 0
}
historical_data = {
    "CPI": deque(maxlen=60),
    "IPC": deque(maxlen=60),
    "Utilization": deque(maxlen=60)
}

def simulate_pipeline():
    """Simulate pipeline performance data"""
    for stage in pipeline_stages:
        pipeline_utilization[stage] = random.uniform(0.5, 0.98)  # more variation

    performance_metrics["CPI"] = round(random.uniform(0.6, 2.5), 2)
    performance_metrics["IPC"] = round(1 / performance_metrics["CPI"], 2)
    performance_metrics["Stalls"] = random.randint(5, 50)
    performance_metrics["BranchMispredict"] = random.randint(2, 20)
    performance_metrics["CacheMisses"] = random.randint(5, 30)

    historical_data["CPI"].append(performance_metrics["CPI"])
    historical_data["IPC"].append(performance_metrics["IPC"])
    historical_data["Utilization"].append(
        sum(pipeline_utilization.values()) / len(pipeline_utilization)
    )

    return {
        "utilization": pipeline_utilization,
        "metrics": performance_metrics,
        "historical": {k: list(v) for k, v in historical_data.items()}
    }

@app.route('/')
def index():
    return render_template('index.html', stages=pipeline_stages)

@app.route('/data')
def get_data():
    return jsonify(simulate_pipeline())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use PORT env variable or fallback to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
