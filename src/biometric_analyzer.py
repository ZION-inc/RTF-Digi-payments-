import numpy as np
from typing import Dict, Optional
from collections import defaultdict

class BiometricAnalyzer:
    def __init__(self):
        self.user_profiles = defaultdict(lambda: {
            'typing_speed': [],
            'swipe_velocity': [],
            'pressure_pattern': [],
            'device_angle': []
        })
    
    def update_profile(self, user_id: str, biometric_data: Dict):
        profile = self.user_profiles[user_id]
        
        for key in ['typing_speed', 'swipe_velocity', 'pressure_pattern', 'device_angle']:
            if key in biometric_data and biometric_data[key] is not None:
                profile[key].append(biometric_data[key])
                # Keep only last 100 samples
                if len(profile[key]) > 100:
                    profile[key] = profile[key][-100:]
    
    def calculate_anomaly_score(self, user_id: str, current_biometric: Dict) -> float:
        if user_id not in self.user_profiles:
            return 0.5  # Unknown user, moderate risk
        
        profile = self.user_profiles[user_id]
        anomaly_scores = []
        
        for key in ['typing_speed', 'swipe_velocity', 'pressure_pattern', 'device_angle']:
            if key in current_biometric and current_biometric[key] is not None:
                if len(profile[key]) >= 5:
                    score = self._calculate_deviation(
                        current_biometric[key],
                        profile[key]
                    )
                    anomaly_scores.append(score)
        
        if not anomaly_scores:
            return 0.5
        
        return np.mean(anomaly_scores)
    
    def _calculate_deviation(self, current_value: float, historical_values: list) -> float:
        if not historical_values:
            return 0.5
        
        mean = np.mean(historical_values)
        std = np.std(historical_values)
        
        if std == 0:
            return 0.0 if abs(current_value - mean) < 0.01 else 1.0
        
        z_score = abs((current_value - mean) / std)
        
        # Convert z-score to probability (0-1)
        if z_score > 3:
            return 0.95
        elif z_score > 2:
            return 0.75
        elif z_score > 1:
            return 0.4
        return 0.1
