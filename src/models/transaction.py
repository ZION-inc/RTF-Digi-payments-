from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class BiometricData(BaseModel):
    typing_speed: Optional[float] = None
    swipe_velocity: Optional[float] = None
    pressure_pattern: Optional[float] = None
    device_angle: Optional[float] = None

class Transaction(BaseModel):
    transaction_id: str
    sender_id: str
    receiver_id: str
    amount: float = Field(gt=0)
    timestamp: datetime
    device_id: str
    ip_address: str
    biometric: Optional[BiometricData] = None
    metadata: Optional[Dict] = None

class FraudScore(BaseModel):
    transaction_id: str
    fraud_probability: float
    ml_score: float
    graph_score: float
    biometric_score: float
    is_fraudulent: bool
    latency_ms: float
    reason: Optional[str] = None
