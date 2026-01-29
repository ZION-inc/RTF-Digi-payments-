# 🚀 Quick Start - Running the System

## Option 1: Run Demo (No Installation Required)

If Python is installed, simply run:

```bash
python demo.py
```

Or double-click: `run_demo.bat`

This will demonstrate:
- ✅ Multi-layer fraud detection
- ✅ Real-time scoring (<500ms)
- ✅ 4 test scenarios
- ✅ Fraud pattern recognition

## Option 2: Full System Setup

### Prerequisites
1. **Install Python 3.8+**
   - Download: https://www.python.org/downloads/
   - ⚠️ Check "Add Python to PATH" during installation

2. **Install Redis**
   - Windows: https://github.com/microsoftarchive/redis/releases
   - Or use Docker: `docker run -d -p 6379:6379 redis:7-alpine`

### Setup Steps

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Redis (in separate terminal)
redis-server

# 3. Train the model
python train_model.py

# 4. Run example
python example_usage.py

# 5. Start API server
python src/api.py
```

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Analyze transaction
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d "{\"transaction_id\":\"TEST001\",\"sender_id\":\"USER001\",\"receiver_id\":\"USER002\",\"amount\":5000.0,\"timestamp\":\"2024-01-01T10:00:00\",\"device_id\":\"DEVICE001\",\"ip_address\":\"192.168.1.1\"}"
```

## Option 3: Docker Deployment

```bash
# Start all services
docker-compose up --build

# API available at http://localhost:8000
```

## 📊 What You'll See

### Demo Output Example:
```
🔹 TEST CASE 1: Normal Transaction
📊 Analyzing Transaction: TXN001
   Sender: USER_ALICE → Receiver: USER_BOB
   Amount: ₹2,500.00

   🔍 Detection Scores:
      ML Score:        0.2500 (weight: 50%)
      Graph Score:     0.1200 (weight: 30%)
      Biometric Score: 0.1500 (weight: 20%)

   📈 Final Results:
      Fraud Probability: 0.1895
      Decision: ✅ LEGITIMATE
      Latency: 2.45ms
```

## 🎯 Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| Latency | <500ms | ✅ |
| ML Scoring | <200ms | ✅ |
| Graph Analysis | <150ms | ✅ |
| Throughput | >1000 TPS | ✅ |

## 📚 Documentation

- **README.md** - Project overview
- **ARCHITECTURE.md** - System design
- **API.md** - API reference
- **DEPLOYMENT.md** - Production deployment

## 🆘 Troubleshooting

### Python not found
- Install Python 3.8+ from python.org
- Add Python to system PATH

### Redis connection error
- Start Redis: `redis-server`
- Or use Docker: `docker run -d -p 6379:6379 redis`

### Module not found
- Install dependencies: `pip install -r requirements.txt`

## 🎉 Ready!

Start with the demo to see the system in action:
```bash
python demo.py
```
