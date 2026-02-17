import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
from rtf_digi_payments.fraud_engine import FraudDetectionEngine
from rtf_digi_payments.models.transaction import Transaction, BiometricData

app = Flask(__name__, 
            template_folder='web/templates',
            static_folder='web/static')
CORS(app)

# Initialize fraud detection engine
engine = FraudDetectionEngine()

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/api/v1/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        
        # Create transaction object
        txn = Transaction(
            transaction_id=data['transaction_id'],
            sender_id=data['sender_id'],
            receiver_id=data['receiver_id'],
            amount=float(data['amount']),
            timestamp=datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00')),
            device_id=data['device_id'],
            ip_address=data['ip_address'],
            biometric=BiometricData(
                typing_speed=data.get('typing_speed', 50.0),
                swipe_velocity=data.get('swipe_velocity', 120.0)
            ) if 'typing_speed' in data or 'swipe_velocity' in data else None
        )
        
        # Analyze transaction
        result = engine.analyze_transaction(txn)
        
        return jsonify({
            'transaction_id': result.transaction_id,
            'fraud_probability': result.fraud_probability,
            'ml_score': result.ml_score,
            'graph_score': result.graph_score,
            'biometric_score': result.biometric_score,
            'is_fraudulent': result.is_fraudulent,
            'latency_ms': result.latency_ms,
            'reason': result.reason
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'fraud-detection-web'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  RTF FRAUD DETECTION - WEB INTERFACE")
    print("="*60)
    print("\n[*] Starting web server...")
    print("[*] Open your browser and visit: http://localhost:5000")
    print("[*] Press Ctrl+C to stop\n")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
