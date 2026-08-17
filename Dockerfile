# 1. Imagen base ligera y segura para producción
FROM python:3.13-slim

# 2. Directorio de trabajo interno en el contenedor
WORKDIR /app

# 3. Dependencias del sistema y limpieza de caché para optimizar peso
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Capa de dependencias de Python (Aprovecha el caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia del código fuente del proyecto
COPY . .

# 6. Exposición del puerto de la API web
EXPOSE 8000