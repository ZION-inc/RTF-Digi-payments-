import networkx as nx
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Tuple, Set

class GraphFraudDetector:
    def __init__(self, window_hours: int = 24, min_ring_size: int = 3):
        self.window_hours = window_hours
        self.min_ring_size = min_ring_size
        self.graph = nx.DiGraph()
        self.transaction_times = defaultdict(list)
        
    def add_transaction(self, sender: str, receiver: str, amount: float, timestamp: datetime):
        if self.graph.has_edge(sender, receiver):
            self.graph[sender][receiver]['weight'] += 1
            self.graph[sender][receiver]['total_amount'] += amount
        else:
            self.graph.add_edge(sender, receiver, weight=1, total_amount=amount)
        
        self.transaction_times[sender].append(timestamp)
        self._cleanup_old_edges(timestamp)
    
    def _cleanup_old_edges(self, current_time: datetime):
        cutoff = current_time - timedelta(hours=self.window_hours)
        nodes_to_remove = [node for node, times in self.transaction_times.items() 
                          if times and max(times) < cutoff]
        self.graph.remove_nodes_from(nodes_to_remove)
        for node in nodes_to_remove:
            del self.transaction_times[node]
    
    def detect_fraud_ring(self, sender: str, receiver: str) -> Tuple[float, Set[str]]:
        if sender not in self.graph or receiver not in self.graph:
            return 0.0, set()
        
        # Check for circular patterns
        try:
            cycle_nodes = set()
            for cycle in nx.simple_cycles(self.graph.subgraph([sender, receiver] + 
                                         list(self.graph.successors(sender)) + 
                                         list(self.graph.predecessors(receiver)))):
                if len(cycle) >= self.min_ring_size:
                    cycle_nodes.update(cycle)
            
            if cycle_nodes:
                return 0.9, cycle_nodes
        except:
            pass
        
        # Check transaction velocity
        velocity_score = self._calculate_velocity_score(sender)
        
        # Check for mule account patterns
        mule_score = self._detect_mule_pattern(receiver)
        
        return max(velocity_score, mule_score), set()
    
    def _calculate_velocity_score(self, node: str) -> float:
        if node not in self.transaction_times:
            return 0.0
        
        recent_txns = [t for t in self.transaction_times[node] 
                      if (datetime.now() - t).total_seconds() < 3600]
        
        if len(recent_txns) > 10:
            return min(len(recent_txns) / 20.0, 1.0)
        return 0.0
    
    def _detect_mule_pattern(self, node: str) -> float:
        if node not in self.graph:
            return 0.0
        
        in_degree = self.graph.in_degree(node)
        out_degree = self.graph.out_degree(node)
        
        if in_degree > 5 and out_degree > 5:
            return 0.8
        elif in_degree > 3 and out_degree > 3:
            return 0.6
        return 0.0
