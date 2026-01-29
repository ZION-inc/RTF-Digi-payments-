# Data Directory

This directory stores training and test data.

## Files

- `training_data.csv` - Generated training dataset (created by data_generator.py)

## Data Generation

To generate training data:

```bash
python src/data_generator.py
```

## Data Schema

| Column | Type | Description |
|--------|------|-------------|
| amount | float | Transaction amount |
| hour | int | Hour of day (0-23) |
| day_of_week | int | Day of week (0-6) |
| amount_log | float | Log-transformed amount |
| sender_txn_count | int | Sender transaction count |
| receiver_txn_count | int | Receiver transaction count |
| amount_velocity | int | Transaction velocity |
| device_change | int | Device change indicator (0/1) |
| ip_change | int | IP change indicator (0/1) |
| is_fraud | int | Fraud label (0/1) |
