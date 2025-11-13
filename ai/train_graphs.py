"""Training harness for ai_quantum_core (prototype).

Uses networkx to construct graphs and extract features for simple ML tasks.
"""

import networkx as nx
import numpy as np
from sklearn.cluster import KMeans


def graph_features(G):
    return np.array([G.number_of_nodes(), G.number_of_edges(), nx.average_clustering(G)])


def demo():
    G = nx.erdos_renyi_graph(100, 0.05)
    feats = graph_features(G)
    print('features', feats)
    km = KMeans(n_clusters=2)
    km.fit(feats.reshape(1, -1))

if __name__ == '__main__':
    demo()
