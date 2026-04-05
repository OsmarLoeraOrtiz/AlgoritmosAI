from sklearn.svm import SVC
from sklearn.datasets import make_moons
from .utils import generate_decision_boundary

class MLController:
    @staticmethod
    def get_svm_visualization(kernel='rbf', C=1.0, gamma='scale'):
        # 1. Generar datos sintéticos de prueba (Moons)
        X, y = make_moons(n_samples=100, noise=0.1, random_state=42)
        
        # 2. Entrenar el modelo con los parámetros recibidos
        model = SVC(kernel=kernel, C=float(C), gamma=gamma)
        model.fit(X, y)
        
        # 3. Generar la frontera de decisión
        grid_data = generate_decision_boundary(model, X)
        
        # 4. Estructurar respuesta para el Frontend
        return {
            "points": {
                "x": X[:, 0].tolist(),
                "y": X[:, 1].tolist(),
                "labels": y.tolist()
            },
            "grid": grid_data
        }