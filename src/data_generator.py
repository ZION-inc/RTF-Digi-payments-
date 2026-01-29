import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_training_data(n_samples=10000, fraud_ratio=0.02):
    np.random.seed(42)
    n_fraud = int(n_samples * fraud_ratio)
    n_normal = n_samples - n_fraud
    
    # Normal transactions
    normal_data = {
        'amount': np.random.lognormal(7, 1.5, n_normal),
        'hour': np.random.choice(range(8, 22), n_normal),
        'day_of_week': np.random.choice(range(7), n_normal),
        'sender_txn_count': np.random.poisson(5, n_normal),
        'receiver_txn_count': np.random.poisson(5, n_normal),
        'amount_velocity': np.random.poisson(2, n_normal),
        'device_change': np.random.choice([0, 1], n_normal, p=[0.95, 0.05]),
        'ip_change': np.random.choice([0, 1], n_normal, p=[0.9, 0.1]),
        'is_fraud': np.zeros(n_normal)
    }
    
    # Fraudulent transactions
    fraud_data = {
        'amount': np.random.lognormal(10, 1, n_fraud),
        'hour': np.random.choice(range(0, 6), n_fraud),
        'day_of_week': np.random.choice(range(7), n_fraud),
        'sender_txn_count': np.random.poisson(15, n_fraud),
        'receiver_txn_count': np.random.poisson(15, n_fraud),
        'amount_velocity': np.random.poisson(8, n_fraud),
        'device_change': np.random.choice([0, 1], n_fraud, p=[0.3, 0.7]),
        'ip_change': np.random.choice([0, 1], n_fraud, p=[0.2, 0.8]),
        'is_fraud': np.ones(n_fraud)
    }
    
    df_normal = pd.DataFrame(normal_data)
    df_fraud = pd.DataFrame(fraud_data)
    df = pd.concat([df_normal, df_fraud], ignore_index=True)
    df['amount_log'] = np.log1p(df['amount'])
    
    return df.sample(frac=1).reset_index(drop=True)

if __name__ == "__main__":
    df = generate_training_data()
    df.to_csv('data/training_data.csv', index=False)
    print(f"Generated {len(df)} samples with {df['is_fraud'].sum()} fraudulent transactions")
