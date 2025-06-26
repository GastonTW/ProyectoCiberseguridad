# 🔐 Trabajo Integrador - Desarrollo Seguro de Aplicaciones

Aplicación vulnerable desarrollada como trabajo integrador para la materia **Desarrollo Seguro de Aplicaciones**. El objetivo es demostrar y corregir vulnerabilidades comunes como **SQL Injection**, **Cross-Site Scripting (XSS)** y **Broken Access Control** dentro de un entorno Docker.

---

## 👨‍💻 Autores

- Tobias Garcia  
- Ulises Pereira  
- Gaston Triviño

---

## 🐳 Docker

La aplicación se ejecuta dentro de un contenedor Docker para facilitar su despliegue.

### Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python init_db.py

EXPOSE 5000
CMD ["python", "app.py"]

### Docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    container_name: ctf_app_team_ptt
    
---
    
## 🏁 Cómo setear la flag
La flag final se define como una variable de entorno.

Editar el archivo /config/.env y cambiar el valor de FLAG:

/config/.env

FLAG=CTF{ejemplo_de_flag}

Luego reiniciar el contenedor para aplicar los cambios.

---

## 🔥 Forma de explotación

## 1. 🐍 SQL Injection (búsqueda)
La aplicación es vulnerable a SQL Injection en el campo de búsqueda principal.

Paso a paso:

Usar sqlmap para detectar la tabla brainrot y la columna rol.

Extraer los usuarios y contraseñas.

Iniciar sesión como un usuario con el rol premium.

Ejemplo de comando con sqlmap:

- sqlmap -u "http://localhost:5000/?nombre=TEST" --method=POST --data="nombre=TEST" --dump -T brainrot -C nombre,contrasenia,rol

## 2. ✴️ XSS en /estadisticas

Una vez logueado como premium, se accede al endpoint /estadisticas, el cual es vulnerable a XSS reflejado.

Payload de ejemplo:

- <script>alert('1')</script>

Esto revela una pista oculta:
Revisá /admin/debug/mostrar/

## 3. 🚪 Broken Access Control
Al acceder a la ruta /admin/debug/mostrar/, si el atacante logra autenticarse como admin, obtiene la flag final.

El endpoint presenta un control de acceso débil que permite saltarse validaciones si se conoce la URL.

---

## 🛠️ Código corregido (Parche)
El repositorio contiene dos ramas:

entrega_vulnerable: versión original con fallos de seguridad.

entrega_patch: versión corregida con buenas prácticas.

En la rama entrega_patch se implementan los siguientes cambios:

## 🔐 Parche 1 - SQL Injection
Uso de consultas parametrizadas para prevenir inyecciones:

- sql = "SELECT id, nombre, imagen FROM brainrot WHERE nombre LIKE ? COLLATE NOCASE"

- param = f"%{nombre}%"

- rows = conn.execute(sql, (param,)).fetchall()

## 🛡️ Parche 2 - XSS
Validación del rol y control de los datos antes de renderizar la vista:

- if role not in ("premium", "admin"):
    return redirect(url_for("home"))

Y la vista solo muestra contenido confiable desde la base.

## 🚫 Parche 3 - Broken Access Control
Chequeo estricto del rol admin antes de mostrar la flag:

- if role != "admin":
    return redirect(url_for("home"))
