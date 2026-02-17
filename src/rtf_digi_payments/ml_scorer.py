import numpy as np
import lightgbm as lgb
import pickle
from pathlib import Path
from typing import Dict

class MLFraudScorer:
    def __init__(self, model_path: str = None):
        self.model = None
        self.feature_names = [
            'amount', 'hour', 'day_of_week', 'amount_log',
            'sender_txn_count', 'receiver_txn_count',
            'amount_velocity', 'device_change', 'ip_change'
        ]
        
        if model_path and Path(model_path).exists():
            self.load_model(model_path)
        else:
            self._init_default_model()
    
    def _init_default_model(self):
        # Lightweight LightGBM for sub-200ms inference
        self.model = lgb.LGBMClassifier(
            n_estimators=50,
            max_depth=6,
            num_leaves=31,
            learning_rate=0.1,
            n_jobs=1,
            verbose=-1
        )
    
    def extract_features(self, transaction: Dict, historical_data: Dict) -> np.ndarray:
        amount = transaction['amount']
        timestamp = transaction['timestamp']
        
        features = [
            amount,
            timestamp.hour,
            timestamp.weekday(),
            np.log1p(amount),
            historical_data.get('sender_txn_count', 0),
            historical_data.get('receiver_txn_count', 0),
            historical_data.get('amount_velocity', 0),
            1 if historical_data.get('device_changed', False) else 0,
            1 if historical_data.get('ip_changed', False) else 0
        ]
        
        return np.array(features).reshape(1, -1)
    
    def predict_fraud_probability(self, features: np.ndarray) -> float:
        if self.model is None:
            return 0.5
        
        try:
            if hasattr(self.model, 'predict_proba'):
                proba = self.model.predict_proba(features)[0][1]
            else:
                # Fallback heuristic scoring
                proba = self._heuristic_score(features[0])
            return float(proba)
        except:
            return self._heuristic_score(features[0])
    
    def _heuristic_score(self, features: np.ndarray) -> float:
        score = 0.0
        
        # High amount transactions
        if features[0] > 50000:
            score += 0.3
        
        # Unusual hours (midnight to 5am)
        if features[1] < 5:
            score += 0.2
        
        # High velocity
        if features[6] > 5:
            score += 0.3
        
        # Device/IP changes
        if features[7] or features[8]:
            score += 0.2
        
        return min(score, 1.0)
    
    def train(self, X: np.ndarray, y: np.ndarray, sample_weight: np.ndarray = None):
        # Handle imbalanced dataset with class weights
        if sample_weight is None:
            fraud_ratio = np.sum(y) / len(y)
            sample_weight = np.where(y == 1, 1.0 / fraud_ratio, 1.0)
        
        self.model.fit(X, y, sample_weight=sample_weight)
    
    def save_model(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)
    
    def load_model(self, path: str):
        with open(path, 'rb') as f:
            self.model = pickle.load(f)
