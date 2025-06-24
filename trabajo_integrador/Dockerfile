# Dockerfile
FROM python:3.11-slim

# Definimos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de requerimientos y lo instalamos
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto al contenedor
COPY . .

# Exponemos el puerto donde corre Flask
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["python", "app.py"]
