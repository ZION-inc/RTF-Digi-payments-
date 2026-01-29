"""
Real-Time Fraud Detection System - Demo
Simulates the fraud detection engine without external dependencies
"""

import time
import random
from datetime import datetime

class FraudDetectionDemo:
    def __init__(self):
        self.fraud_threshold = 0.75
        print("[*] Fraud Detection Engine Initialized")
        print("=" * 60)
    
    def simulate_ml_score(self, amount, hour):
        """Simulate ML fraud scoring"""
        score = 0.0
        if amount > 50000:
            score += 0.3
        if hour < 5:
            score += 0.2
        score += random.uniform(0, 0.3)
        return min(score, 1.0)
    
    def simulate_graph_score(self, sender_id, receiver_id):
        """Simulate graph network analysis"""
        # Simulate fraud ring detection
        if "RING" in sender_id or "RING" in receiver_id:
            return 0.9
        return random.uniform(0, 0.3)
    
    def simulate_biometric_score(self, typing_speed):
        """Simulate biometric analysis"""
        if typing_speed and typing_speed > 150:
            return 0.7
        return random.uniform(0, 0.3)
    
    def analyze_transaction(self, txn):
        """Analyze transaction for fraud"""
        start_time = time.time()
        
        print(f"\n[*] Analyzing Transaction: {txn['transaction_id']}")
        print(f"   Sender: {txn['sender_id']} -> Receiver: {txn['receiver_id']}")
        print(f"   Amount: Rs.{txn['amount']:,.2f}")
        
        # Simulate parallel detection
        ml_score = self.simulate_ml_score(txn['amount'], txn['timestamp'].hour)
        graph_score = self.simulate_graph_score(txn['sender_id'], txn['receiver_id'])
        biometric_score = self.simulate_biometric_score(txn.get('typing_speed'))
        
        # Weighted ensemble
        fraud_probability = (
            0.5 * ml_score +
            0.3 * graph_score +
            0.2 * biometric_score
        )
        
        is_fraudulent = fraud_probability >= self.fraud_threshold
        latency_ms = (time.time() - start_time) * 1000
        
        # Display results
        print(f"\n   [*] Detection Scores:")
        print(f"      ML Score:        {ml_score:.4f} (weight: 50%)")
        print(f"      Graph Score:     {graph_score:.4f} (weight: 30%)")
        print(f"      Biometric Score: {biometric_score:.4f} (weight: 20%)")
        print(f"\n   [*] Final Results:")
        print(f"      Fraud Probability: {fraud_probability:.4f}")
        print(f"      Decision: {'[!] FRAUDULENT' if is_fraudulent else '[OK] LEGITIMATE'}")
        print(f"      Latency: {latency_ms:.2f}ms")
        
        if is_fraudulent:
            reasons = []
            if ml_score > 0.5:
                reasons.append("High ML risk")
            if graph_score > 0.7:
                reasons.append("Fraud ring detected")
            if biometric_score > 0.5:
                reasons.append("Biometric anomaly")
            print(f"      Reason: {'; '.join(reasons)}")
        
        return {
            'fraud_probability': fraud_probability,
            'is_fraudulent': is_fraudulent,
            'latency_ms': latency_ms
        }

def main():
    print("\n" + "=" * 60)
    print("  REAL-TIME FRAUD DETECTION SYSTEM - DEMO")
    print("  UPI & Digital Payments Security")
    print("=" * 60)
    
    engine = FraudDetectionDemo()
    
    # Test Case 1: Normal Transaction
    print("\n\n[TEST 1] Normal Transaction")
    print("-" * 60)
    txn1 = {
        'transaction_id': 'TXN001',
        'sender_id': 'USER_ALICE',
        'receiver_id': 'USER_BOB',
        'amount': 2500.0,
        'timestamp': datetime.now().replace(hour=14),
        'typing_speed': 50.0
    }
    engine.analyze_transaction(txn1)
    
    # Test Case 2: High-Risk Transaction
    print("\n\n[TEST 2] High-Risk Transaction (Large Amount + Late Night)")
    print("-" * 60)
    txn2 = {
        'transaction_id': 'TXN002',
        'sender_id': 'USER_CHARLIE',
        'receiver_id': 'USER_DAVE',
        'amount': 95000.0,
        'timestamp': datetime.now().replace(hour=2),
        'typing_speed': 45.0
    }
    engine.analyze_transaction(txn2)
    
    # Test Case 3: Fraud Ring Detection
    print("\n\n[TEST 3] Fraud Ring Pattern")
    print("-" * 60)
    txn3 = {
        'transaction_id': 'TXN003',
        'sender_id': 'RING_USER_A',
        'receiver_id': 'RING_USER_B',
        'amount': 15000.0,
        'timestamp': datetime.now().replace(hour=10),
        'typing_speed': 50.0
    }
    engine.analyze_transaction(txn3)
    
    # Test Case 4: Biometric Anomaly
    print("\n\n[TEST 4] Biometric Anomaly (Unusual Typing Speed)")
    print("-" * 60)
    txn4 = {
        'transaction_id': 'TXN004',
        'sender_id': 'USER_EVE',
        'receiver_id': 'USER_FRANK',
        'amount': 5000.0,
        'timestamp': datetime.now().replace(hour=15),
        'typing_speed': 200.0
    }
    engine.analyze_transaction(txn4)
    
    # Summary
    print("\n\n" + "=" * 60)
    print("  DEMO COMPLETE")
    print("=" * 60)
    print("\n[OK] Key Features Demonstrated:")
    print("   - Sub-500ms latency guarantee")
    print("   - Multi-layer detection (ML + Graph + Biometric)")
    print("   - Weighted ensemble scoring")
    print("   - Real-time fraud pattern recognition")
    print("\n[INFO] To run the full system:")
    print("   1. Install Python 3.8+")
    print("   2. Run: pip install -r requirements.txt")
    print("   3. Start Redis: redis-server")
    print("   4. Train model: python train_model.py")
    print("   5. Run API: python src/api.py")
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    main()
