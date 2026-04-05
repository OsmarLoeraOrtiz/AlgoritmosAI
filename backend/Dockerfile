# Usamos una imagen ligera de Python
FROM python:3.12-slim

# Evita que Python genere archivos .pyc y permite logueo en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalar dependencias del sistema (necesarias para psycopg2 y compilaciones de ML)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto de Django
EXPOSE 8000

# Comando por defecto (puedes sobrescribirlo en docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]