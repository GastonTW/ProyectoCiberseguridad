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
        ("Tung tung tung Sahur", "Tung_tung_tung_sahur.png", 90, 30, 70, 10, 30, 100),
        ("Tralalero Tralala", "Traralelo_tralala.png", 70, 70, 40, 50, 10, 85),
        ("Ballerina Capuccina", "ballerina-capuccina.png", 40, 100, 480, 80, 60, 50),
        ("Bombardino Crocodilo", "Bombardino_crocodilo.png", 100, 30, 50, 30, 10, 90),
        ("Brr Brr Patapim", "Brr_brr_patapim.png", 60, 60, 60, 100, 80, 70),
        ("Lirila Larila", "Lirili_larila.png", 90, 10, 90, 80, 70, 40),
        ("Desarrollinni Segurinni", "Desarrollinni_segurinni.png", 75, 75, 75, 75, 50, 0),
    ]
)


c.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", [
    ("admin", "supersecret", "admin"),
    ("premium", "brbrpatapim", "premium"),
    ("usuario1", "asd123", "user")
])

conn.commit()
conn.close()
