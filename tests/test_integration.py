import pytest
import requests
from datetime import datetime
from rtf_digi_payments.models.transaction import Transaction, BiometricData
from rtf_digi_payments.fraud_engine import FraudDetectionEngine

class TestIntegration:
    @pytest.fixture
    def engine(self):
        return FraudDetectionEngine()
    
    def test_end_to_end_normal_flow(self, engine):
        txn = Transaction(
            transaction_id="INT_001",
            sender_id="ALICE",
            receiver_id="BOB",
            amount=1500.0,
            timestamp=datetime.now(),
            device_id="DEV_ALICE",
            ip_address="192.168.1.10",
            biometric=BiometricData(typing_speed=45.0, swipe_velocity=120.0)
        )
        
        result = engine.analyze_transaction(txn)
        
        assert result.transaction_id == "INT_001"
        assert result.latency_ms < 500
        assert 0 <= result.fraud_probability <= 1
        assert result.ml_score >= 0
        assert result.graph_score >= 0
        assert result.biometric_score >= 0
    
    def test_fraud_ring_scenario(self, engine):
        users = ["RING_1", "RING_2", "RING_3", "RING_4"]
        
        for i in range(10):
            sender = users[i % len(users)]
            receiver = users[(i + 1) % len(users)]
            
            txn = Transaction(
                transaction_id=f"RING_{i}",
                sender_id=sender,
                receiver_id=receiver,
                amount=15000.0,
                timestamp=datetime.now(),
                device_id=f"DEV_{sender}",
                ip_address=f"10.0.0.{i}"
            )
            
            result = engine.analyze_transaction(txn)
        
        assert result.graph_score > 0.0
    
    def test_high_velocity_detection(self, engine):
        for i in range(15):
            txn = Transaction(
                transaction_id=f"VEL_{i}",
                sender_id="VELOCITY_USER",
                receiver_id=f"RECV_{i}",
                amount=5000.0,
                timestamp=datetime.now(),
                device_id="DEV_VEL",
                ip_address="192.168.1.100"
            )
            
            result = engine.analyze_transaction(txn)
        
        assert result.graph_score > 0.3
    
    def test_biometric_consistency(self, engine):
        bio = BiometricData(typing_speed=50.0, swipe_velocity=100.0)
        
        for i in range(5):
            txn = Transaction(
                transaction_id=f"BIO_{i}",
                sender_id="BIO_USER",
                receiver_id=f"RECV_{i}",
                amount=2000.0,
                timestamp=datetime.now(),
                device_id="DEV_BIO",
                ip_address="192.168.1.50",
                biometric=bio
            )
            
            result = engine.analyze_transaction(txn)
        
        assert result.biometric_score < 0.5
    
    def test_device_change_detection(self, engine):
        txn1 = Transaction(
            transaction_id="DEV_1",
            sender_id="DEV_USER",
            receiver_id="RECV_1",
            amount=3000.0,
            timestamp=datetime.now(),
            device_id="DEVICE_A",
            ip_address="192.168.1.1"
        )
        engine.analyze_transaction(txn1)
        
        txn2 = Transaction(
            transaction_id="DEV_2",
            sender_id="DEV_USER",
            receiver_id="RECV_2",
            amount=3000.0,
            timestamp=datetime.now(),
            device_id="DEVICE_B",
            ip_address="192.168.1.1"
        )
        result = engine.analyze_transaction(txn2)
        
        assert result.ml_score > 0.0
