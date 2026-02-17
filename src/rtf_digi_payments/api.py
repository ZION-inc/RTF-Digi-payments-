from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from .fraud_engine import FraudDetectionEngine
from .models.transaction import Transaction, FraudScore
import uvicorn

app = FastAPI(title="Real-Time Fraud Detection API")
engine = FraudDetectionEngine()

@app.post("/api/v1/analyze", response_model=FraudScore)
async def analyze_transaction(transaction: Transaction):
    try:
        result = engine.analyze_transaction(transaction)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fraud-detection"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4)
