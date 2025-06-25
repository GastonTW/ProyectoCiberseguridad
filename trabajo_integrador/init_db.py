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
    imagen TEXT,
    fuerza INTEGER,
    velocidad INTEGER,
    resistencia INTEGER,
    inteligencia INTEGER,
    carisma INTEGER,
    aura INTEGER
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
c.executemany(
    "INSERT INTO brainrot (nombre, imagen, fuerza, velocidad, resistencia, inteligencia, carisma, aura) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    [
        ("Tung", "img1.png", 90, 10, 70, 10, 30, 100),
        ("Tralalero", "img2.png", 70, 70, 40, 50, 10, 85),
    ]
)


c.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", [
    ("admin", "supersecret", "admin"),
    ("premium", "brainrotdude", "premium"),
    ("visitante", "lol123", "user")
])

conn.commit()
conn.close()
