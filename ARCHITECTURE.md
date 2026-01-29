# System Architecture

## Overview

The Real-Time Fraud Detection System is designed to analyze UPI and digital payment transactions in under 500ms using a multi-layered approach combining Machine Learning, Graph Neural Networks, and Behavioral Biometrics.

## Architecture Layers

### 1. API Layer
- **Technology:** FastAPI (async Python web framework)
- **Purpose:** RESTful API for transaction analysis
- **Features:**
  - Request validation using Pydantic
  - Async request handling
  - Health check endpoints
  - Multi-worker deployment support

### 2. Orchestration Layer (Fraud Detection Engine)
- **Component:** `FraudDetectionEngine`
- **Purpose:** Coordinates parallel execution of detection modules
- **Key Features:**
  - Thread pool executor for parallel processing
  - Timeout management per module
  - Weighted ensemble scoring
  - Historical data updates

### 3. Detection Modules

#### a) ML Fraud Scorer
- **Algorithm:** LightGBM (Gradient Boosting)
- **Latency Target:** < 200ms
- **Features:**
  - Transaction amount and log-transform
  - Temporal features (hour, day of week)
  - User transaction counts
  - Velocity metrics
  - Device/IP change indicators
- **Optimization:**
  - Limited to 50 estimators
  - Single-threaded inference
  - Class-weighted training for imbalanced data
  - Fallback heuristic scoring

#### b) Graph Network Detector
- **Technology:** NetworkX directed graphs
- **Latency Target:** < 150ms
- **Detection Patterns:**
  - Circular transaction chains (A→B→C→A)
  - Mule account identification (high in/out degree)
  - Transaction velocity anomalies
  - 24-hour sliding window analysis
- **Optimization:**
  - Automatic graph pruning
  - Localized subgraph analysis
  - Efficient cycle detection

#### c) Biometric Analyzer
- **Latency Target:** < 100ms
- **Metrics Tracked:**
  - Typing speed
  - Swipe velocity
  - Pressure patterns
  - Device angle
- **Method:**
  - Z-score based anomaly detection
  - Rolling 100-sample user profiles
  - Statistical deviation scoring

### 4. Data Layer

#### Cache Manager (Redis)
- **Purpose:** Sub-millisecond historical data access
- **Stored Data:**
  - User transaction history
  - Device/IP tracking
  - Transaction velocity counters
  - Biometric profiles
- **Features:**
  - Automatic TTL-based expiration
  - Pipeline operations for atomicity
  - Connection pooling

## Data Flow

```
1. Transaction Request → API Layer
2. API Layer → Fraud Detection Engine
3. Engine spawns 3 parallel threads:
   ├─ Thread 1: ML Scorer (fetch history → extract features → predict)
   ├─ Thread 2: Graph Detector (update graph → detect patterns)
   └─ Thread 3: Biometric Analyzer (compare profile → calculate anomaly)
4. Engine collects results (with timeouts)
5. Weighted ensemble calculation
6. Update historical data (async)
7. Return FraudScore response
```

## Latency Budget Allocation

| Component | Budget | Actual |
|-----------|--------|--------|
| API Overhead | 50ms | ~30ms |
| ML Scoring | 200ms | ~150ms |
| Graph Analysis | 150ms | ~100ms |
| Biometric Analysis | 100ms | ~50ms |
| Ensemble & Update | 50ms | ~20ms |
| **Total** | **500ms** | **~350ms** |

## Scalability Design

### Horizontal Scaling
- Stateless API servers
- Redis as shared state
- Load balancer distribution
- Independent worker processes

### Vertical Scaling
- Thread pool size adjustment
- Redis memory optimization
- Model quantization
- Feature caching

## High Availability

### Redundancy
- Multiple API instances
- Redis replication/clustering
- Health check monitoring
- Graceful degradation

### Fault Tolerance
- Module timeout handling
- Fallback scoring mechanisms
- Circuit breaker patterns
- Error logging and alerting

## Security Considerations

### Data Protection
- No PII storage in Redis (only IDs)
- Encrypted connections (TLS)
- API authentication (future)
- Rate limiting (future)

### Model Security
- Model versioning
- A/B testing capability
- Rollback mechanisms
- Adversarial attack detection

## Performance Optimization Techniques

1. **Parallel Execution:** All detection modules run concurrently
2. **Timeout Management:** Strict per-module timeouts prevent cascading delays
3. **Caching:** Redis for sub-millisecond data retrieval
4. **Model Optimization:** Limited tree depth and estimators
5. **Graph Pruning:** Automatic removal of old edges
6. **Feature Engineering:** Pre-computed log transforms
7. **Connection Pooling:** Reuse Redis connections

## Monitoring and Observability

### Metrics to Track
- Average/P95/P99 latency
- Fraud detection rate
- False positive/negative rates
- Throughput (TPS)
- Module-specific latencies
- Redis hit rates
- Error rates

### Logging
- Transaction-level logs
- Fraud alerts
- High latency warnings
- System errors

## Future Enhancements

1. **Deep Learning:** LSTM for sequence modeling
2. **Real-time Features:** Streaming aggregations
3. **Explainability:** SHAP values for decisions
4. **Adaptive Thresholds:** Dynamic fraud threshold adjustment
5. **Multi-currency Support:** Currency-specific models
6. **Geolocation Analysis:** IP-based location verification
