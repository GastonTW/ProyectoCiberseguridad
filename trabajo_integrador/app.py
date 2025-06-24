# app.py
from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/search/brainrot")
def brainrot_search():
    nombre = request.args.get("nombre", "")
    conn = get_db_connection()

    # ❌ vulnerable a SQLi
    query = f"SELECT id, nombre, imagen FROM brainrot WHERE nombre LIKE '%{nombre}%'"
    try:
        rows = conn.execute(query).fetchall()
    except Exception as e:
        return f"<p>Error en la consulta: {e}</p>"

    return render_template("search.html", rows=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)