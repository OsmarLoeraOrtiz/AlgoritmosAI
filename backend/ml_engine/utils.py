import numpy as np

def generate_decision_boundary(model, X, resolution=0.1):
    """
    Genera una malla (grid) para visualizar las fronteras de decisión.
    """
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    
    # Crear la rejilla
    xx, yy = np.meshgrid(
        np.arange(x_min, x_max, resolution),
        np.arange(y_min, y_max, resolution)
    )
    
    # Predecir sobre cada punto de la rejilla
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    return {
        "x": xx.tolist(), # Convertimos a lista para JSON
        "y": yy.tolist(),
        "z": Z.tolist(),
    }