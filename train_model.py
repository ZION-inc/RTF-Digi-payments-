import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
from src.ml_scorer import MLFraudScorer
from src.data_generator import generate_training_data
import os

def train_model():
    print("Generating training data...")
    df = generate_training_data(n_samples=50000, fraud_ratio=0.02)
    
    feature_cols = ['amount', 'hour', 'day_of_week', 'amount_log',
                    'sender_txn_count', 'receiver_txn_count',
                    'amount_velocity', 'device_change', 'ip_change']
    
    X = df[feature_cols].values
    y = df['is_fraud'].values
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")
    print(f"Fraud ratio: {y_train.mean():.4f}")
    
    scorer = MLFraudScorer()
    print("\nTraining model...")
    scorer.train(X_train, y_train)
    
    print("\nEvaluating model...")
    y_pred_proba = np.array([scorer.predict_fraud_probability(x.reshape(1, -1)) for x in X_test])
    y_pred = (y_pred_proba > 0.5).astype(int)
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print(f"\nROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")
    print(f"\nConfusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
    
    os.makedirs('models', exist_ok=True)
    scorer.save_model('models/fraud_model.pkl')
    print("\nModel saved to models/fraud_model.pkl")

if __name__ == "__main__":
    train_model()
