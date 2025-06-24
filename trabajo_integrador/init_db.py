import sqlite3
import os

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/database.db")
c = conn.cursor()

# Tablas
c.execute("DROP TABLE IF EXISTS brainrot")
c.execute("DROP TABLE IF EXISTS users")

c.execute("""
CREATE TABLE brainrot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    imagen TEXT
)
""")

c.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
""")

# Datos
c.executemany("INSERT INTO brainrot (nombre, imagen) VALUES (?, ?)", [
    ("Tung", "img1.png"),
    ("Tralalero", "img2.png"),
])

c.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", [
    ("admin", "supersecret", "admin"),
    ("premium", "brainrotdude", "premium"),
    ("visitante", "lol123", "user")
])

conn.commit()
conn.close()
