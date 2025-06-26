# 🔐 Trabajo Integrador - Desarrollo Seguro de Aplicaciones

Aplicación vulnerable desarrollada como trabajo integrador para la materia **Desarrollo Seguro de Aplicaciones**. El objetivo es demostrar y corregir vulnerabilidades comunes como **SQL Injection**, **Cross-Site Scripting (XSS)** y **Broken Access Control** dentro de un entorno Docker.

---

## 👨‍💻 Autores

- Tobias García  
- Ulises Pereira  
- Gastón Triviño

---

## 🐳 Docker

La aplicación se ejecuta dentro de un contenedor Docker para facilitar su despliegue.

### Dockerfile
```
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python init_db.py

EXPOSE 5000
CMD ["python", "app.py"]
```

### Docker-compose.yml
```
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    container_name: ctf_app_team_ptt
```
---
    
## 🏁 Cómo setear la flag
La flag final se define como una variable de entorno.

Editar el archivo /config/.env y cambiar el valor de FLAG:

` /config/.env `
``` 
FLAG=flag{ejemplo_de_flag}
```

Luego reiniciar el contenedor para aplicar los cambios.

---

## 🔥 Forma de explotación

## 1. 🐍 SQL Injection (búsqueda)
La aplicación es vulnerable a **SQL Injection** en el campo de búsqueda principal de la página, que aparece en la pantalla de inicio o en la pestaña de búsqueda.

Paso a paso para utilizar esta vulnerabilidad:

- Listar tabla users.
- Extraer los usuarios y contraseñas.
- Probar los diferentes usuarios.
- Iniciar sesión como un usuario con el rol **premium**.

*Existen **pistas** en el html de la pagina.*

Ejemplo de payload:
```
' UNION SELECT username,password,role FROM  users  -- 
```

## 2. ✴️ XSS en /estadisticas

Una vez logueado como premium, se accede a la funcion de *estadisticas*, la cual es vulnerable a **XSS reflejado**.

Payload de ejemplo:

```<script>alert('1')</script>```

Esto revela una pista oculta:
*Revisá **/admin/debug/mostrar/***

## 3. 🚪 Broken Access Control
Al acceder a la ruta `/admin/debug/mostrar/`, no pasará nada. Sin embargo, en `/admin/debug/mostrar/[id]` se mostrarán los datos de los diferentes personajes cargados accediendo desde cualquier usuario, siendo que solo debería ser visible para el administrador. Al ver los datos de "Desarrollinni Segurinni", se podrá ver la flag en el campo *descripción*. La vulnerabilidad resulta redundante, pues se puede acceder a esta pestaña ingresando desde el usuario *admin*, pero sí resulta necesaria de arreglar al hacer el parche.

---

## 🛠️ Código corregido (Parche)
El repositorio contiene dos ramas:

`entrega_vulnerable`: versión original con fallos de seguridad.

`entrega_patch`: versión corregida con buenas prácticas.

En la rama entrega_patch se implementan los siguientes cambios:

## 🔐 Parche 1 - SQL Injection
Uso de consultas parametrizadas para prevenir inyecciones:

```python
#app.py
@app.route("/search/brainrot")
def brainrot_search():
    nombre = request.args.get("nombre", "")
    conn = get_db_connection()

    sql = """
        SELECT id, nombre, imagen
        FROM brainrot
        WHERE nombre LIKE ?
        COLLATE NOCASE
    """
    param = f"%{nombre}%"
    try:
        rows = conn.execute(sql, (param,)).fetchall()
    except Exception as e:
        return f"<p>Error en la consulta: {e}</p>"
    finally:
        conn.close()

    return render_template("search.html", rows=rows)
```

## 🛡️ Parche 2 - XSS
En la app, hay validación del rol y control de los datos antes de renderizar la vista:

```python
#app.py
@app.route("/estadisticas", methods=["GET", "POST"])
def estadisticas():
    role = session.get("role")
    if role not in ("premium", "admin"):
        return redirect(url_for("home"))
    nombre = ""
    stats = None
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        conn = get_db_connection()
        row = conn.execute("""
            SELECT nombre, imagen, fuerza, velocidad, resistencia, inteligencia, carisma, aura
            FROM brainrot WHERE nombre = ? COLLATE NOCASE
        """, (nombre,)).fetchone()
        conn.close()

        stats = dict(row) if row else {"nombre": nombre, "error": "No se encontró ese brainrot"}
    secret = "Revisa /admin/debug/mostrar/"
    return render_template("estadisticas.html", stats=stats, secret=secret)
```

En la vista, solo se muestra contenido confiable desde la base.
```html
<!-- estadisticas.html -->
{% extends 'base.html' %}

{% block title %}
  Estadísticas de {{ stats.nombre }}
{% endblock %}

{% block content %}
<h1 class="text-center mb-4">📊 Estadísticas de {{ stats.nombre }}</h1>
<!-- Codigo -->
{% if stats %}
  {% if stats.error %}
    <div class="alert alert-warning">{{ stats.error }}</div>
  {% else %}
    <div class="card mx-auto" style="max-width:500px;">
      <div class="card-body text-center">
        <h4 class="card-title mb-3">{{ stats.nombre }}</h4>
        <div class="card card-full img-container mb-3">
          <img src="{{ url_for('static', filename='brainrots/' ~ stats.imagen) }}"
               alt="{{ stats.nombre }}" class="img-fluid">
        </div>
        <ul class="list-group list-group-flush text-start">
          {% for label, value in [
              ('Fuerza', stats.fuerza),
              ('Velocidad', stats.velocidad),
              ('Resistencia', stats.resistencia),
              ('Inteligencia', stats.inteligencia),
              ('Carisma', stats.carisma),
              ('Aura', stats.aura)
            ]
          %}
          <li class="list-group-item">
            <div class="d-flex justify-content-between">
              <span>{{ label }}</span>
              <span>{{ value }}%</span>
            </div>
            <div class="progress" style="height: 1rem;">
              <div class="progress-bar bg-primary" role="progressbar"
                   style="width: {{ value }}%;" aria-valuenow="{{ value }}"
                   aria-valuemin="0" aria-valuemax="100">
              </div>
            </div>
          </li>
          {% endfor %}
        </ul>
      </div>
    </div>
  {% endif %}
{% else %}
  <!-- Codigo -->
{% endif %}
  <!-- Codigo -->
{% endblock %}
```

## 🚫 Parche 3 - Broken Access Control
Chequeo estricto del rol admin antes de mostrar la página:

```python
#app.py
@app.route('/admin/debug/mostrar/<int:id>')
def mostrar_brainrot(id):
    role = session.get("role")
    if role not in ("admin"):
        return redirect(url_for("home"))
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM brainrot WHERE id = ?", (id,))
    brainrot = cursor.fetchone()
    conn.close()

    if not brainrot:
        return "Brainrot no encontrado", 404

    brainrot = list(brainrot)  # Convertimos a lista para poder modificar
    if brainrot[0] == 7:
         brainrot[9] = os.environ.get('FLAG')

    return render_template('mostrar_brainrot.html', brainrot=brainrot)
```
