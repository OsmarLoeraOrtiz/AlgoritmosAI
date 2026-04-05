# ML Visualizer Dashboard 🚀

Esta aplicación es una plataforma interactiva diseñada para la visualización de modelos de Machine Learning en tiempo real. Permite a los usuarios ajustar hiperparámetros desde una interfaz web y observar instantáneamente cómo cambian las fronteras de decisión o los resultados del modelo mediante gráficos dinámicos.

---

## 🏗️ Arquitectura del Sistema

El proyecto sigue una arquitectura de N-Capas desacoplada, facilitando la escalabilidad del motor de ML y la persistencia de datos.

```mermaid
graph TD
    subgraph "Frontend (Cliente)"
        A[Navegador / App] --> B[Dashboard UI]
        B --> C[Plotly.js Render]
    end
    subgraph "Backend Container (Django + DRF)"
        C -- "Petición API JSON" --> D[DRF Endpoints]
        D --> E[Serializers: Validación de Hiperparámetros]
        E --> F[ML Controller]

        subgraph "ML Engine"
            F --> G[Scikit-Learn Model]
            G --> H[Numpy Matrix Processor]
        end

        H -- "Resultados Arrays" --> E
        E -- "Respuesta Estructurada JSON" --> C
    end
    subgraph "Persistencia"
        D --> I[(PostgreSQL: Datasets & Config)]
        F --> J[(Redis: Cache de Predicciones)]
    end
```

### Componentes Principales

| Componente | Tecnología | Responsabilidad |
|---|---|---|
| **Frontend** | React / JS + Plotly.js | Renderizado interactivo de gráficas y matrices de datos |
| **Backend** | Django REST Framework | Orquestación, validación de hiperparámetros y exposición de la API |
| **ML Engine** | Scikit-Learn + Numpy | Cómputo de modelos y manipulación de matrices (Decision Boundaries) |
| **Base de Datos** | PostgreSQL | Almacena configuraciones, metadatos de modelos y datasets |
| **Caché** | Redis | Evita el re-entrenamiento ante peticiones con parámetros idénticos |

---

## 🔄 Flujo de Comunicación (Request-Response)

El siguiente diagrama detalla el ciclo de vida de una petición cuando un usuario solicita una visualización específica (ej. un SVM con kernel RBF).

```mermaid
sequenceDiagram
    participant FE as Frontend (JS/React)
    participant API as DRF ViewSet
    participant SER as Serializer
    participant ML as ML Engine (Python)

    FE->>API: GET /api/v1/visualize/?algo=svm&kernel=rbf&c=1.0
    API->>SER: Validar Parámetros de URL
    alt Parámetros Inválidos
        SER-->>API: raise ValidationError
        API-->>FE: 400 Bad Request (JSON Error)
    else Parámetros Correctos
        SER->>ML: ejecutar_svc(kernel='rbf', c=1.0)
        ML->>ML: Generar Grid & Predict
        ML-->>SER: Retorna Diccionario (X, Y, Z_mesh)
        SER-->>API: Transforma Arrays a Listas JSON
        API-->>FE: 200 OK + Payload JSON
        FE->>FE: Plotly.react(data)
    end
```

> **Nota técnica:** Los Serializers de Django juegan un papel crítico aquí, transformando los `ndarrays` de Numpy (no serializables) en listas estándar de Python para poder ser enviadas vía JSON.

---

## 🐳 Infraestructura y Despliegue

La aplicación está completamente dockerizada para garantizar la paridad entre los entornos de desarrollo y producción.

```mermaid
graph LR
    subgraph "Docker Network"
        direction LR
        Proxy[Nginx]
        API[Django + DRF + ML]
        DB[(PostgreSQL)]
        Worker[Celery Worker*]
    end
    Client((Internet)) --> Proxy
    Proxy --> API
    API --> DB
    API -.-> Worker

    style Worker stroke-dasharray: 5 5
```

| Servicio | Rol |
|---|---|
| **Nginx** | Proxy Inverso: maneja la terminación SSL y sirve archivos estáticos |
| **Django + ML** | Contenedor core que ejecuta la lógica de negocio |
| **Celery Worker** | *(Opcional)* Tareas de entrenamiento pesado fuera del ciclo HTTP |
