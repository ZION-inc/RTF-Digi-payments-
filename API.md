# API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Analyze Transaction

Analyzes a transaction for fraud in real-time.

**Endpoint:** `POST /api/v1/analyze`

**Request Body:**
```json
{
  "transaction_id": "string (required)",
  "sender_id": "string (required)",
  "receiver_id": "string (required)",
  "amount": "float (required, > 0)",
  "timestamp": "ISO 8601 datetime (required)",
  "device_id": "string (required)",
  "ip_address": "string (required)",
  "biometric": {
    "typing_speed": "float (optional)",
    "swipe_velocity": "float (optional)",
    "pressure_pattern": "float (optional)",
    "device_angle": "float (optional)"
  },
  "metadata": "object (optional)"
}
```

**Response:**
```json
{
  "transaction_id": "TXN001",
  "fraud_probability": 0.85,
  "ml_score": 0.78,
  "graph_score": 0.92,
  "biometric_score": 0.65,
  "is_fraudulent": true,
  "latency_ms": 245.67,
  "reason": "High ML risk score; Fraud ring detected"
}
```

**Status Codes:**
- `200 OK`: Transaction analyzed successfully
- `422 Unprocessable Entity`: Invalid request data
- `500 Internal Server Error`: Processing error

**Example:**
```python
import requests
from datetime import datetime

response = requests.post(
    "http://localhost:8000/api/v1/analyze",
    json={
        "transaction_id": "TXN123",
        "sender_id": "USER001",
        "receiver_id": "USER002",
        "amount": 15000.0,
        "timestamp": datetime.now().isoformat(),
        "device_id": "DEVICE_A",
        "ip_address": "192.168.1.10",
        "biometric": {
            "typing_speed": 45.0,
            "swipe_velocity": 120.0
        }
    }
)

result = response.json()
print(f"Fraud Probability: {result['fraud_probability']}")
```

### 2. Health Check

Checks if the service is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "fraud-detection"
}
```

**Status Codes:**
- `200 OK`: Service is healthy

## Response Fields

### FraudScore Object

| Field | Type | Description |
|-------|------|-------------|
| transaction_id | string | Unique transaction identifier |
| fraud_probability | float | Overall fraud probability (0-1) |
| ml_score | float | Machine learning model score (0-1) |
| graph_score | float | Graph network analysis score (0-1) |
| biometric_score | float | Biometric anomaly score (0-1) |
| is_fraudulent | boolean | True if fraud_probability >= threshold |
| latency_ms | float | Processing time in milliseconds |
| reason | string | Explanation if fraudulent (null otherwise) |

## Fraud Detection Logic

The system uses a weighted ensemble approach:

```
fraud_probability = (0.5 × ml_score) + (0.3 × graph_score) + (0.2 × biometric_score)
```

**Decision Threshold:** 0.75 (configurable)

## Performance Guarantees

- **Latency:** < 500ms (99th percentile)
- **Throughput:** > 1000 TPS
- **Availability:** 99.9% uptime

## Rate Limiting

No rate limiting in current version. Implement at load balancer level for production.

## Error Handling

All errors return JSON with structure:
```json
{
  "detail": "Error message description"
}
```

## Client Libraries

### Python Client
```python
from client import FraudDetectionClient

client = FraudDetectionClient("http://localhost:8000")
result = client.analyze_transaction(
    transaction_id="TXN001",
    sender_id="USER_A",
    receiver_id="USER_B",
    amount=5000.0,
    device_id="DEV001",
    ip_address="192.168.1.1"
)
```

## Monitoring Endpoints

Future versions will include:
- `/metrics` - Prometheus metrics
- `/stats` - Real-time statistics
- `/admin/model` - Model management
