# Real-Time Fraud Detection System for UPI & Digital Payments

A high-performance fraud detection engine capable of analyzing transactions in **<500ms** using Graph Neural Networks, Machine Learning, and Behavioral Biometrics.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Transaction Input                         │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │  Fraud Detection      │
         │  Engine (Parallel)    │
         └───────────┬───────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼────┐    ┌─────▼─────┐   ┌─────▼──────┐
│   ML   │    │   Graph   │   │ Biometric  │
│ Scorer │    │ Detector  │   │  Analyzer  │
│<200ms  │    │  <150ms   │   │   <100ms   │
└───┬────┘    └─────┬─────┘   └─────┬──────┘
    │                │                │
    └────────────────┼────────────────┘
                     │
              ┌──────▼──────┐
              │   Weighted  │
              │   Ensemble  │
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │ Fraud Score │
              │  + Decision │
              └─────────────┘
```

## Core Components

### 1. Graph Network Detector
- Identifies fraud rings using NetworkX directed graphs
- Detects circular transaction patterns (mule accounts)
- Calculates transaction velocity scores
- 24-hour sliding window for pattern analysis

### 2. ML Fraud Scorer
- LightGBM classifier optimized for <200ms inference
- Handles imbalanced datasets with class weighting
- Feature extraction: amount, time, velocity, device changes
- Fallback heuristic scoring for robustness

### 3. Biometric Analyzer
- Validates user identity via behavioral patterns
- Tracks: typing speed, swipe velocity, pressure, device angle
- Z-score based anomaly detection
- Maintains rolling 100-sample user profiles

### 4. Cache Manager
- Redis-backed historical data storage
- Sub-millisecond user history retrieval
- Transaction velocity tracking
- Automatic TTL-based cleanup

## Installation

```bash
pip install -r requirements.txt
```

**Prerequisites:**
- Python 3.8+
- Redis server running on localhost:6379

## Usage

### API Server
```bash
python src/api.py
```

### Example Request
```python
import requests
from datetime import datetime

transaction = {
    "transaction_id": "TXN123",
    "sender_id": "USER001",
    "receiver_id": "USER002",
    "amount": 5000.0,
    "timestamp": datetime.now().isoformat(),
    "device_id": "DEVICE001",
    "ip_address": "192.168.1.1",
    "biometric": {
        "typing_speed": 50.0,
        "swipe_velocity": 120.0
    }
}

response = requests.post("http://localhost:8000/api/v1/analyze", json=transaction)
print(response.json())
```

### Programmatic Usage
```python
from src.fraud_engine import FraudDetectionEngine
from src.models.transaction import Transaction

engine = FraudDetectionEngine()
result = engine.analyze_transaction(transaction)

print(f"Fraud Probability: {result.fraud_probability}")
print(f"Latency: {result.latency_ms}ms")
```

## Performance Characteristics

| Metric | Target | Achieved |
|--------|--------|----------|
| End-to-End Latency | <500ms | ✓ |
| ML Scoring | <200ms | ✓ |
| Graph Analysis | <150ms | ✓ |
| Throughput | >1000 TPS | ✓ |

## Configuration

Edit `config/settings.py`:

```python
FRAUD_THRESHOLD = 0.75          # Decision threshold
MAX_LATENCY_MS = 500            # Total latency budget
ML_SCORING_TIMEOUT_MS = 200     # ML module timeout
GRAPH_ANALYSIS_TIMEOUT_MS = 150 # Graph module timeout

# Ensemble weights
BIOMETRIC_WEIGHT = 0.2
ML_SCORE_WEIGHT = 0.5
GRAPH_SCORE_WEIGHT = 0.3
```

## Testing

```bash
pytest tests/test_fraud_engine.py -v
```

## Key Features

✓ **Sub-500ms Latency**: Parallel execution with timeouts  
✓ **Fraud Ring Detection**: Graph-based pattern recognition  
✓ **Imbalanced Data Handling**: Class-weighted training  
✓ **Behavioral Biometrics**: User identity validation  
✓ **Scalable Architecture**: Redis caching + async processing  
✓ **Production Ready**: FastAPI REST API with health checks  

## Fraud Detection Patterns

1. **Circular Transactions**: A→B→C→A patterns
2. **Mule Accounts**: High in-degree + out-degree nodes
3. **Velocity Anomalies**: >10 transactions/hour
4. **Biometric Deviations**: Z-score > 2 from baseline
5. **Device/IP Changes**: Sudden context switches
6. **Unusual Timing**: Transactions at 12am-5am
7. **High Amounts**: Transactions >₹50,000

## License

MIT
