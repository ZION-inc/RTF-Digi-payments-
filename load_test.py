import asyncio
import aiohttp
import time
from datetime import datetime
import numpy as np

async def send_transaction(session, transaction_id):
    payload = {
        "transaction_id": f"LOAD_{transaction_id}",
        "sender_id": f"USER_{transaction_id % 1000}",
        "receiver_id": f"USER_{(transaction_id + 1) % 1000}",
        "amount": float(np.random.uniform(100, 50000)),
        "timestamp": datetime.now().isoformat(),
        "device_id": f"DEV_{transaction_id % 100}",
        "ip_address": f"192.168.{transaction_id % 255}.{(transaction_id + 1) % 255}",
        "biometric": {
            "typing_speed": float(np.random.uniform(30, 80)),
            "swipe_velocity": float(np.random.uniform(80, 150))
        }
    }
    
    start = time.time()
    try:
        async with session.post('http://localhost:8000/api/v1/analyze', json=payload) as response:
            result = await response.json()
            latency = (time.time() - start) * 1000
            return {'success': True, 'latency': latency}
    except Exception as e:
        return {'success': False, 'error': str(e)}

async def load_test(n_requests=1000, concurrency=50):
    print(f"Starting load test: {n_requests} requests with {concurrency} concurrent connections\n")
    
    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        start_time = time.time()
        
        tasks = [send_transaction(session, i) for i in range(n_requests)]
        results = await asyncio.gather(*tasks)
        
        total_time = time.time() - start_time
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    latencies = [r['latency'] for r in successful]
    
    print("=== Load Test Results ===\n")
    print(f"Total Requests: {n_requests}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    print(f"Success Rate: {len(successful)/n_requests*100:.2f}%")
    print(f"\nTotal Time: {total_time:.2f}s")
    print(f"Throughput: {n_requests/total_time:.2f} TPS")
    
    if latencies:
        print(f"\nLatency Statistics:")
        print(f"  Mean: {np.mean(latencies):.2f}ms")
        print(f"  Median: {np.median(latencies):.2f}ms")
        print(f"  95th Percentile: {np.percentile(latencies, 95):.2f}ms")
        print(f"  99th Percentile: {np.percentile(latencies, 99):.2f}ms")
        print(f"  Max: {np.max(latencies):.2f}ms")

if __name__ == "__main__":
    asyncio.run(load_test(n_requests=1000, concurrency=50))
