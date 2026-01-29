import pytest
from datetime import datetime
from src.fraud_engine import FraudDetectionEngine
from src.models.transaction import Transaction, BiometricData

@pytest.fixture
def engine():
    return FraudDetectionEngine()

def test_normal_transaction(engine):
    txn = Transaction(
        transaction_id="TXN001",
        sender_id="USER001",
        receiver_id="USER002",
        amount=1000.0,
        timestamp=datetime.now(),
        device_id="DEV001",
        ip_address="192.168.1.1"
    )
    
    result = engine.analyze_transaction(txn)
    
    assert result.latency_ms < 500
    assert 0 <= result.fraud_probability <= 1
    assert not result.is_fraudulent

def test_high_amount_transaction(engine):
    txn = Transaction(
        transaction_id="TXN002",
        sender_id="USER003",
        receiver_id="USER004",
        amount=100000.0,
        timestamp=datetime.now(),
        device_id="DEV002",
        ip_address="192.168.1.2"
    )
    
    result = engine.analyze_transaction(txn)
    assert result.ml_score > 0.3

def test_fraud_ring_detection(engine):
    # Create circular transaction pattern
    for i in range(5):
        txn = Transaction(
            transaction_id=f"TXN{i}",
            sender_id=f"USER{i}",
            receiver_id=f"USER{(i+1)%5}",
            amount=5000.0,
            timestamp=datetime.now(),
            device_id=f"DEV{i}",
            ip_address=f"192.168.1.{i}"
        )
        engine.analyze_transaction(txn)
    
    # Final transaction should detect ring
    final_txn = Transaction(
        transaction_id="TXN_FINAL",
        sender_id="USER0",
        receiver_id="USER1",
        amount=5000.0,
        timestamp=datetime.now(),
        device_id="DEV0",
        ip_address="192.168.1.0"
    )
    
    result = engine.analyze_transaction(final_txn)
    assert result.graph_score > 0.0

def test_biometric_anomaly(engine):
    # Establish baseline
    bio_normal = BiometricData(
        typing_speed=50.0,
        swipe_velocity=100.0,
        pressure_pattern=0.5
    )
    
    for i in range(10):
        txn = Transaction(
            transaction_id=f"TXN_BIO_{i}",
            sender_id="USER_BIO",
            receiver_id=f"USER_{i}",
            amount=1000.0,
            timestamp=datetime.now(),
            device_id="DEV_BIO",
            ip_address="192.168.1.100",
            biometric=bio_normal
        )
        engine.analyze_transaction(txn)
    
    # Anomalous biometric
    bio_anomaly = BiometricData(
        typing_speed=200.0,
        swipe_velocity=500.0,
        pressure_pattern=2.0
    )
    
    txn_anomaly = Transaction(
        transaction_id="TXN_ANOMALY",
        sender_id="USER_BIO",
        receiver_id="USER_TARGET",
        amount=1000.0,
        timestamp=datetime.now(),
        device_id="DEV_BIO",
        ip_address="192.168.1.100",
        biometric=bio_anomaly
    )
    
    result = engine.analyze_transaction(txn_anomaly)
    assert result.biometric_score > 0.5

def test_latency_constraint(engine):
    txn = Transaction(
        transaction_id="TXN_LATENCY",
        sender_id="USER_LATENCY",
        receiver_id="USER_RECEIVER",
        amount=5000.0,
        timestamp=datetime.now(),
        device_id="DEV_LATENCY",
        ip_address="192.168.1.50"
    )
    
    result = engine.analyze_transaction(txn)
    assert result.latency_ms < 500, f"Latency {result.latency_ms}ms exceeds 500ms threshold"
