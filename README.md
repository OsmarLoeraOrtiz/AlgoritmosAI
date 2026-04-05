# Arquitectura ML Visualizer — Modelo C4

---

## Nivel 1: Diagrama de Contexto

Muestra cómo el sistema interactúa con el mundo exterior.

```mermaid
C4Context
    title Diagrama de Contexto: ML Visualizer System

    Person(user, "Estudiante/Data Scientist", "Usuario que desea visualizar fronteras de decisión de algoritmos de ML clásicos.")
    System(ml_app, "ML Visualizer Platform", "Permite configurar hiperparámetros, cargar datasets y renderizar visualizaciones matemáticas interactivas.")

    System_Ext(datasets, "OpenML / UCI Repositories", "Fuentes externas de datasets para pruebas (opcional).")

    Rel(user, ml_app, "Configura parámetros y visualiza resultados", "HTTPS/JSON")
    Rel(ml_app, datasets, "Descarga datasets de referencia", "Python API")
```

---

## Nivel 2: Diagrama de Contenedores

Muestra la infraestructura dentro de Docker y cómo DRF controla la comunicación.

```mermaid
C4Container
    title Diagrama de Contenedores: ML Visualizer

    Container(ui, "Frontend SPA", "React / Plotly.js", "Interfaz de usuario reactiva para el control de gráficas.")

    ContainerBoundary(c1, "Docker Cluster") {
        Container(api, "API Server (Django + DRF)", "Python, Gunicorn", "Expone endpoints REST, gestiona autenticación y lógica de negocio.")
        Container(worker, "ML Engine", "Scikit-Learn, NumPy", "Módulo especializado en computación matemática y entrenamiento de modelos.")
        ContainerDb(db, "Database", "PostgreSQL", "Almacena metadatos de datasets y configuraciones de experimentos.")
        Container(cache, "Cache", "Redis", "Almacena resultados de fronteras de decisión pesadas para acceso rápido.")
    }

    Rel(ui, api, "Peticiones de inferencia y visualización", "JSON/HTTPS")
    Rel(api, worker, "Llama funciones de entrenamiento", "In-process call")
    Rel(api, db, "Lectura/Escritura", "SQL")
    Rel(api, cache, "Persistencia temporal", "Protocolo Redis")
```

---

## Nivel 3: Diagrama de Componentes

Desglosa cómo se organiza Django REST Framework para procesar la IA.

```mermaid
C4Component
    title Diagrama de Componentes: API Server (Django)

    Component(ser, "Serializers", "DRF Serializer", "Valida los hiperparámetros (C, gamma, k) enviados por el usuario.")
    Component(view, "ML ViewSets", "DRF APIViews", "Orquesta la petición, maneja el flujo de datos.")
    Component(engine, "Calculation Engine", "Python Module", "Calcula la matriz de predicciones (Z-mesh) para el gráfico.")
    Component(store, "Model Registry", "Django Models", "Gestiona la ubicación de los archivos CSV y metadatos.")

    Rel(view, ser, "Valida input")
    Rel(view, engine, "Solicita computación de frontera")
    Rel(view, store, "Consulta datos del dataset")
    Rel(engine, view, "Retorna coordenadas JSON")
```

---

## Diagrama de Secuencia: Flujo de Inferencia

Detalla la interacción exacta desde que el usuario hace clic hasta que el gráfico se actualiza.

```mermaid
sequenceDiagram
    autonumber
    participant U as Usuario (Browser)
    participant F as Frontend (Plotly.js)
    participant A as DRF API (Django)
    participant E as ML Engine (Scikit-Learn)
    participant C as Redis Cache

    U->>F: Cambia Kernel de SVM a 'RBF'
    F->>A: POST /api/visualize/svm/ {gamma: 0.1, C: 1.0}

    A->>C: Existe calculo previo para estos parametros?
    alt Cache Hit
        C-->>A: Retorna Matriz Z
    else Cache Miss
        A->>E: Entrenar SVC(kernel='rbf', gamma=0.1)
        E->>E: Generar Grid Mesh (np.meshgrid)
        E->>E: model.predict(grid)
        E-->>A: Retorna Coordenadas y Predicciones
        A->>C: Guardar resultado (expira en 1h)
    end

    A-->>F: HTTP 200 OK {data: [...], layout: {...}}
    F->>U: Renderiza nueva frontera de decision
```
