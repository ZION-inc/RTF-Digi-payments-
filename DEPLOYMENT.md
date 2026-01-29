# Deployment Guide

## Quick Start

### 1. Local Development Setup

```bash
# Clone repository
git clone <repository-url>
cd "RTF Digi payments"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Redis
redis-server

# Run the system
python example_usage.py
```

### 2. Train ML Model

```bash
python train_model.py
```

This generates a trained LightGBM model at `models/fraud_model.pkl`.

### 3. Start API Server

```bash
python src/api.py
```

API will be available at `http://localhost:8000`

### 4. Run Tests

```bash
# Unit tests
pytest tests/test_fraud_engine.py -v

# Integration tests
pytest tests/test_integration.py -v

# All tests
pytest -v
```

### 5. Performance Benchmarking

```bash
# Latency benchmark
python benchmark.py

# Load testing (requires API running)
python load_test.py
```

## Docker Deployment

### Build and Run with Docker Compose

```bash
docker-compose up --build
```

This starts:
- Redis on port 6379
- Fraud Detection API on port 8000

### Individual Docker Build

```bash
docker build -t fraud-detection .
docker run -p 8000:8000 --env-file .env fraud-detection
```

## Production Deployment

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

### Scaling Considerations

1. **Horizontal Scaling**: Deploy multiple API instances behind a load balancer
2. **Redis Clustering**: Use Redis Cluster for high availability
3. **Model Updates**: Hot-reload models without downtime
4. **Monitoring**: Integrate with Prometheus/Grafana

### Health Checks

```bash
curl http://localhost:8000/health
```

### API Usage

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "TXN001",
    "sender_id": "USER001",
    "receiver_id": "USER002",
    "amount": 5000.0,
    "timestamp": "2024-01-01T10:00:00",
    "device_id": "DEVICE001",
    "ip_address": "192.168.1.1",
    "biometric": {
      "typing_speed": 50.0,
      "swipe_velocity": 120.0
    }
  }'
```

## Monitoring and Logging

Logs are stored in `logs/fraud_detection.log`

Monitor key metrics:
- Average latency
- Fraud detection rate
- Throughput (TPS)
- Error rates

## Performance Tuning

### Redis Optimization
- Enable persistence: `appendonly yes`
- Set appropriate maxmemory policy
- Use connection pooling

### API Optimization
- Adjust worker count based on CPU cores
- Enable HTTP/2
- Use connection keep-alive

### ML Model Optimization
- Reduce n_estimators if latency is high
- Use model quantization
- Cache feature extraction results

## Troubleshooting

### High Latency
- Check Redis connection
- Verify thread pool size
- Monitor CPU/memory usage

### Low Accuracy
- Retrain model with more data
- Adjust ensemble weights
- Fine-tune fraud threshold

### Redis Connection Errors
- Verify Redis is running: `redis-cli ping`
- Check connection settings in config/settings.py
