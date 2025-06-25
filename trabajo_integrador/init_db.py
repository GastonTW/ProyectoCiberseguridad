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
    aura INTEGER,
    descripcion TEXT
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
    "INSERT INTO brainrot (nombre, imagen, fuerza, velocidad, resistencia, inteligencia, carisma, aura, descripcion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
    [
        ("Tung tung tung Sahur", "Tung_tung_tung_sahur.png", 90, 30, 70, 10, 30, 100,
         """Tung tung tung tung tung tung tung tung tung l'alba
Un'anomalia terrificante che appare solo all'alba"""),
        ("Tralalero Tralala", "Traralelo_tralala.png", 70, 70, 40, 50, 10, 85, "Tralalero Tralala, porco Dio e porco Allah. Ero con il mio fottuto figlio Merdardo a giocare a Fortnite, quando a un punto arriva mia nonna"),
        ("Ballerina Capuccina", "ballerina-capuccina.png", 40, 100, 480, 80, 60, 50, "Ballerina Capuchina mi mi mi. È la moglie di Cappuccino Assassino"),
        ("Bombardino Crocodilo", "Bombardino_crocodilo.png", 100, 30, 50, 30, 10, 90, "Bombardiro Crocodilo, un fottuto alligatore volante, che vola e bombarda.Si nutre dello spirito di tua madre."),
        ("Brr Brr Patapim", "Brr_brr_patapim.png", 60, 60, 60, 100, 80, 70, "Brr, brr, Patapim, il mio cappello è pieno di Slim! Nel bosco fitto e misterioso, viveva un essere assai curioso."),
        ("Lirila Larila", "Lirili_larila.png", 90, 10, 90, 80, 70, 40, "Lirilí Larilà, elefante nel deserto che cammina qua e là. Con la sua conchiglia e un orologio che fa tic tac, le spine del cactus mi fanno"),
        ("Desarrollinni Segurinni", "Desarrollinni_segurinni.png", 75, 75, 75, 75, 50, 0, "Desarrollinni Segurinni descripcion"),
    ]
)



c.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", [
    ("admin", "supersecret", "admin"),
    ("premium", "brbrpatapim", "premium"),
    ("usuario1", "asd123", "user")
])

conn.commit()
conn.close()
