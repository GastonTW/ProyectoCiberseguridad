# app.py
from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import random
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="config/.env")  # carga FLAG desde ese archivo


app = Flask(__name__)
app.secret_key = 'supersecretkey123'

def get_db_connection():
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]
        conn = get_db_connection()
        row = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (user, pwd)
        ).fetchone()
        conn.close()
        if row:
            session["username"] = row["username"]
            session["role"] = row["role"]
            return redirect(url_for("home"))
        else:
            error = "Credenciales inválidas"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/search/brainrot")
def brainrot_search():
    nombre = request.args.get("nombre", "")
    conn = get_db_connection()

    query = f"SELECT id, nombre, imagen FROM brainrot WHERE nombre LIKE '%{nombre}%' COLLATE NOCASE"

    try:
        rows = conn.execute(query).fetchall()
    except Exception as e:
        return f"<p>Error en la consulta: {e}</p>"

    return render_template("search.html", rows=rows)

@app.route("/premium", methods=["GET", "POST"])
def premium():
    role = session.get("role")
    if role not in ("premium", "admin"):
        return redirect(url_for("home"))
    if request.method == "POST":
        brainrot1 = request.form["brainrot1"]
        brainrot2 = request.form["brainrot2"]
        conn = get_db_connection()
        cursor = conn.cursor()
        # Verificar si los brainrots existen en la base de datos
        cursor.execute("SELECT * FROM brainrot WHERE nombre = ? COLLATE NOCASE", (brainrot1,))
        row1 = cursor.fetchone()
        cursor.execute("SELECT * FROM brainrot WHERE nombre = ? COLLATE NOCASE", (brainrot2,))
        row2 = cursor.fetchone()
        if row1 and row2:
            winner = random.choice([row1, row2])
            return render_template("premium.html", brainrot1=row1, brainrot2=row2, winner=winner)
        else:
            error_message = "Uno o ambos brainrots no existen en la base de datos."
            return render_template("premium.html", error_message=error_message)
    return render_template("premium.html", brainrot1=None, brainrot2=None, winner=None)

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
    return render_template("estadisticas.html", stats=stats, query=nombre, secret=secret)

@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    results = []

    if query:
        for _, value in movies.items():
            if query.lower() in value['title'].lower():
                results.append({'title': value['title'], 'image': value['image']})

    return render_template('search.html', query=query, results=results)


@app.route('/admin/debug/mostrar/<int:id>')
def mostrar_brainrot(id):
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)