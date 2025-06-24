# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ejecuta init_db.py una vez para generar database.db
RUN python init_db.py

EXPOSE 5000
CMD ["python", "app.py"]



