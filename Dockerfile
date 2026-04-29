# Imagen base
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar e instalar dependencias primero (mejor uso de caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app.py .

# Exponer el puerto
EXPOSE 5000

# Variables de entorno para producción
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Comando para iniciar la app
CMD ["python", "app.py"]
