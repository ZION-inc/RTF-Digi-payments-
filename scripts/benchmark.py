import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import numpy as np
from datetime import datetime
from rtf_digi_payments.fraud_engine import FraudDetectionEngine
from rtf_digi_payments.models.transaction import Transaction, BiometricData

def benchmark_latency(n_transactions=1000):
    engine = FraudDetectionEngine()
    latencies = []
    
    print(f"Running benchmark with {n_transactions} transactions...\n")
    
    for i in range(n_transactions):
        txn = Transaction(
            transaction_id=f"BENCH_{i}",
            sender_id=f"USER_{i % 100}",
            receiver_id=f"USER_{(i + 1) % 100}",
            amount=np.random.uniform(100, 50000),
            timestamp=datetime.now(),
            device_id=f"DEV_{i % 50}",
            ip_address=f"192.168.{i % 255}.{(i + 1) % 255}",
            biometric=BiometricData(
                typing_speed=np.random.uniform(30, 80),
                swipe_velocity=np.random.uniform(80, 150)
            )
        )
        
        result = engine.analyze_transaction(txn)
        latencies.append(result.latency_ms)
    
    latencies = np.array(latencies)
    
    print("=== Performance Benchmark Results ===\n")
    print(f"Total Transactions: {n_transactions}")
    print(f"Mean Latency: {latencies.mean():.2f}ms")
    print(f"Median Latency: {np.median(latencies):.2f}ms")
    print(f"95th Percentile: {np.percentile(latencies, 95):.2f}ms")
    print(f"99th Percentile: {np.percentile(latencies, 99):.2f}ms")
    print(f"Max Latency: {latencies.max():.2f}ms")
    print(f"Min Latency: {latencies.min():.2f}ms")
    
    under_500ms = (latencies < 500).sum()
    print(f"\nTransactions under 500ms: {under_500ms}/{n_transactions} ({under_500ms/n_transactions*100:.2f}%)")
    
    if latencies.mean() < 500:
        print("\n[OK] PASSED: Average latency under 500ms")
    else:
        print("\n[FAIL] FAILED: Average latency exceeds 500ms")
    
    throughput = n_transactions / (latencies.sum() / 1000)
    print(f"\nEstimated Throughput: {throughput:.0f} TPS")

if __name__ == "__main__":
    benchmark_latency(1000)
