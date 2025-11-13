"""Model stub for ai_quantum_core. This is a placeholder for graph-based models.
"""

class GraphModel:
    def __init__(self):
        self.trained = False

    def fit(self, X, y=None):
        self.trained = True

    def predict(self, X):
        if not self.trained:
            raise RuntimeError('Model not trained')
        return [0 for _ in range(len(X))]
