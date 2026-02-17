import matplotlib.pyplot as plt
import networkx as nx

class FraudVisualizer:
    @staticmethod
    def plot_transaction_graph(graph_detector, output_path='fraud_network.png'):
        plt.figure(figsize=(12, 8))
        G = graph_detector.graph
        
        if len(G.nodes()) == 0:
            print("No transactions to visualize")
            return
        
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Node colors based on degree
        node_colors = []
        for node in G.nodes():
            degree = G.in_degree(node) + G.out_degree(node)
            if degree > 10:
                node_colors.append('red')
            elif degree > 5:
                node_colors.append('orange')
            else:
                node_colors.append('lightblue')
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500, alpha=0.8)
        nx.draw_networkx_edges(G, pos, alpha=0.3, arrows=True, arrowsize=15)
        nx.draw_networkx_labels(G, pos, font_size=8)
        
        plt.title("Transaction Network - Fraud Ring Detection", fontsize=14)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Graph saved to {output_path}")
    
    @staticmethod
    def plot_fraud_scores(results, output_path='fraud_scores.png'):
        import numpy as np
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        fraud_probs = [r.fraud_probability for r in results]
        ml_scores = [r.ml_score for r in results]
        graph_scores = [r.graph_score for r in results]
        biometric_scores = [r.biometric_score for r in results]
        
        axes[0, 0].hist(fraud_probs, bins=30, color='red', alpha=0.7)
        axes[0, 0].set_title('Fraud Probability Distribution')
        axes[0, 0].set_xlabel('Probability')
        
        axes[0, 1].hist(ml_scores, bins=30, color='blue', alpha=0.7)
        axes[0, 1].set_title('ML Score Distribution')
        axes[0, 1].set_xlabel('Score')
        
        axes[1, 0].hist(graph_scores, bins=30, color='green', alpha=0.7)
        axes[1, 0].set_title('Graph Score Distribution')
        axes[1, 0].set_xlabel('Score')
        
        axes[1, 1].hist(biometric_scores, bins=30, color='purple', alpha=0.7)
        axes[1, 1].set_title('Biometric Score Distribution')
        axes[1, 1].set_xlabel('Score')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Scores plot saved to {output_path}")
