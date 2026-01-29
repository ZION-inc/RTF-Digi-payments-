import redis
import json
from typing import Dict, Optional
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self, host: str = 'localhost', port: int = 6379, ttl: int = 3600):
        try:
            self.redis_client = redis.Redis(host=host, port=port, decode_responses=True, socket_connect_timeout=1)
            self.redis_client.ping()
            self.use_redis = True
        except:
            self.use_redis = False
            self.cache = {}
        self.ttl = ttl
    
    def get_user_history(self, user_id: str) -> Dict:
        key = f"user:{user_id}:history"
        
        if self.use_redis:
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
        else:
            if key in self.cache:
                return self.cache[key]
        
        return {
            'txn_count': 0,
            'last_device': None,
            'last_ip': None,
            'amount_velocity': 0,
            'last_txn_time': None
        }
    
    def update_user_history(self, user_id: str, transaction: Dict):
        history = self.get_user_history(user_id)
        
        history['txn_count'] += 1
        history['device_changed'] = (history['last_device'] != transaction['device_id'])
        history['ip_changed'] = (history['last_ip'] != transaction['ip_address'])
        history['last_device'] = transaction['device_id']
        history['last_ip'] = transaction['ip_address']
        
        # Calculate velocity
        if history['last_txn_time']:
            last_time = datetime.fromisoformat(history['last_txn_time'])
            time_diff = (transaction['timestamp'] - last_time).total_seconds() / 60
            if time_diff < 60:
                history['amount_velocity'] = history.get('amount_velocity', 0) + 1
            else:
                history['amount_velocity'] = 0
        
        history['last_txn_time'] = transaction['timestamp'].isoformat()
        
        key = f"user:{user_id}:history"
        if self.use_redis:
            self.redis_client.setex(key, self.ttl, json.dumps(history))
        else:
            self.cache[key] = history
        
        return history
    
    def get_transaction_count(self, user_id: str, window_minutes: int = 60) -> int:
        key = f"user:{user_id}:txn_window"
        if self.use_redis:
            count = self.redis_client.get(key)
            return int(count) if count else 0
        else:
            return self.cache.get(key, 0)
    
    def increment_transaction_count(self, user_id: str, window_minutes: int = 60):
        key = f"user:{user_id}:txn_window"
        if self.use_redis:
            pipe = self.redis_client.pipeline()
            pipe.incr(key)
            pipe.expire(key, window_minutes * 60)
            pipe.execute()
        else:
            self.cache[key] = self.cache.get(key, 0) + 1
