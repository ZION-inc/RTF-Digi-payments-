import time
from typing import Dict
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from datetime import datetime

from src.graph_detector import GraphFraudDetector
from src.ml_scorer import MLFraudScorer
from src.biometric_analyzer import BiometricAnalyzer
from src.utils.cache_manager import CacheManager
from src.models.transaction import Transaction, FraudScore
from config.settings import *

class FraudDetectionEngine:
    def __init__(self):
        self.graph_detector = GraphFraudDetector(GRAPH_WINDOW_HOURS, MIN_FRAUD_RING_SIZE)
        self.ml_scorer = MLFraudScorer()
        self.biometric_analyzer = BiometricAnalyzer()
        self.cache_manager = CacheManager(REDIS_HOST, REDIS_PORT, REDIS_TTL)
        self.executor = ThreadPoolExecutor(max_workers=3)
    
    def analyze_transaction(self, transaction: Transaction) -> FraudScore:
        start_time = time.time()
        
        # Parallel execution of detection modules
        ml_future = self.executor.submit(self._ml_analysis, transaction)
        graph_future = self.executor.submit(self._graph_analysis, transaction)
        biometric_future = self.executor.submit(self._biometric_analysis, transaction)
        
        # Collect results with timeout
        try:
            ml_score = ml_future.result(timeout=ML_SCORING_TIMEOUT_MS / 1000)
        except TimeoutError:
            ml_score = 0.5
        
        try:
            graph_score = graph_future.result(timeout=GRAPH_ANALYSIS_TIMEOUT_MS / 1000)
        except TimeoutError:
            graph_score = 0.0
        
        try:
            biometric_score = biometric_future.result(timeout=0.1)
        except TimeoutError:
            biometric_score = 0.5
        
        # Weighted ensemble scoring
        fraud_probability = (
            ML_SCORE_WEIGHT * ml_score +
            GRAPH_SCORE_WEIGHT * graph_score +
            BIOMETRIC_WEIGHT * biometric_score
        )
        
        is_fraudulent = fraud_probability >= FRAUD_THRESHOLD
        latency_ms = (time.time() - start_time) * 1000
        
        # Update historical data
        self._update_history(transaction)
        
        reason = self._generate_reason(ml_score, graph_score, biometric_score) if is_fraudulent else None
        
        return FraudScore(
            transaction_id=transaction.transaction_id,
            fraud_probability=round(fraud_probability, 4),
            ml_score=round(ml_score, 4),
            graph_score=round(graph_score, 4),
            biometric_score=round(biometric_score, 4),
            is_fraudulent=is_fraudulent,
            latency_ms=round(latency_ms, 2),
            reason=reason
        )
    
    def _ml_analysis(self, transaction: Transaction) -> float:
        sender_history = self.cache_manager.get_user_history(transaction.sender_id)
        receiver_history = self.cache_manager.get_user_history(transaction.receiver_id)
        
        historical_data = {
            'sender_txn_count': sender_history['txn_count'],
            'receiver_txn_count': receiver_history['txn_count'],
            'amount_velocity': sender_history.get('amount_velocity', 0),
            'device_changed': sender_history.get('device_changed', False),
            'ip_changed': sender_history.get('ip_changed', False)
        }
        
        txn_dict = {
            'amount': transaction.amount,
            'timestamp': transaction.timestamp
        }
        
        features = self.ml_scorer.extract_features(txn_dict, historical_data)
        return self.ml_scorer.predict_fraud_probability(features)
    
    def _graph_analysis(self, transaction: Transaction) -> float:
        self.graph_detector.add_transaction(
            transaction.sender_id,
            transaction.receiver_id,
            transaction.amount,
            transaction.timestamp
        )
        
        score, fraud_ring = self.graph_detector.detect_fraud_ring(
            transaction.sender_id,
            transaction.receiver_id
        )
        
        return score
    
    def _biometric_analysis(self, transaction: Transaction) -> float:
        if not transaction.biometric:
            return 0.5
        
        biometric_dict = transaction.biometric.dict()
        anomaly_score = self.biometric_analyzer.calculate_anomaly_score(
            transaction.sender_id,
            biometric_dict
        )
        
        self.biometric_analyzer.update_profile(transaction.sender_id, biometric_dict)
        
        return anomaly_score
    
    def _update_history(self, transaction: Transaction):
        txn_dict = {
            'device_id': transaction.device_id,
            'ip_address': transaction.ip_address,
            'timestamp': transaction.timestamp
        }
        
        self.cache_manager.update_user_history(transaction.sender_id, txn_dict)
        self.cache_manager.update_user_history(transaction.receiver_id, txn_dict)
        self.cache_manager.increment_transaction_count(transaction.sender_id)
    
    def _generate_reason(self, ml_score: float, graph_score: float, biometric_score: float) -> str:
        reasons = []
        
        if ml_score > 0.7:
            reasons.append("High ML risk score")
        if graph_score > 0.7:
            reasons.append("Fraud ring detected")
        if biometric_score > 0.7:
            reasons.append("Biometric anomaly")
        
        return "; ".join(reasons) if reasons else "Multiple risk factors"
