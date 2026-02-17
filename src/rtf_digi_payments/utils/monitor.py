import logging
from typing import Dict
import json

class FraudMonitor:
    def __init__(self, log_file='logs/fraud_detection.log'):
        self.logger = logging.getLogger('FraudDetection')
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)
        
        self.stats = {
            'total_transactions': 0,
            'fraud_detected': 0,
            'avg_latency': 0,
            'total_latency': 0
        }
    
    def log_transaction(self, transaction_id: str, result: Dict):
        self.stats['total_transactions'] += 1
        self.stats['total_latency'] += result['latency_ms']
        self.stats['avg_latency'] = self.stats['total_latency'] / self.stats['total_transactions']
        
        if result['is_fraudulent']:
            self.stats['fraud_detected'] += 1
            self.logger.warning(f"FRAUD DETECTED - {transaction_id}: {json.dumps(result)}")
        else:
            self.logger.info(f"Transaction {transaction_id} processed - Latency: {result['latency_ms']}ms")
    
    def get_stats(self) -> Dict:
        return {
            **self.stats,
            'fraud_rate': self.stats['fraud_detected'] / max(self.stats['total_transactions'], 1)
        }
    
    def alert_high_latency(self, transaction_id: str, latency_ms: float, threshold: float = 500):
        if latency_ms > threshold:
            self.logger.error(f"HIGH LATENCY ALERT - {transaction_id}: {latency_ms}ms (threshold: {threshold}ms)")
