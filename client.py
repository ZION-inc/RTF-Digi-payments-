import requests
from typing import Dict, Optional
from datetime import datetime

class FraudDetectionClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def analyze_transaction(self, 
                          transaction_id: str,
                          sender_id: str,
                          receiver_id: str,
                          amount: float,
                          device_id: str,
                          ip_address: str,
                          timestamp: Optional[datetime] = None,
                          biometric: Optional[Dict] = None) -> Dict:
        
        if timestamp is None:
            timestamp = datetime.now()
        
        payload = {
            "transaction_id": transaction_id,
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "amount": amount,
            "timestamp": timestamp.isoformat(),
            "device_id": device_id,
            "ip_address": ip_address
        }
        
        if biometric:
            payload["biometric"] = biometric
        
        response = self.session.post(
            f"{self.base_url}/api/v1/analyze",
            json=payload,
            timeout=2
        )
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> Dict:
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

# Example usage
if __name__ == "__main__":
    client = FraudDetectionClient()
    
    result = client.analyze_transaction(
        transaction_id="CLIENT_001",
        sender_id="USER_A",
        receiver_id="USER_B",
        amount=5000.0,
        device_id="DEVICE_001",
        ip_address="192.168.1.1",
        biometric={"typing_speed": 50.0, "swipe_velocity": 120.0}
    )
    
    print(f"Fraud Probability: {result['fraud_probability']}")
    print(f"Is Fraudulent: {result['is_fraudulent']}")
    print(f"Latency: {result['latency_ms']}ms")
