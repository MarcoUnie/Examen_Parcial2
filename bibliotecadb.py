import sqlite3
def crear_base_datos():
    with sqlite3.connect("biblioteca.db") as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                autor TEXT,
                genero TEXT,
                prestado INTEGER DEFAULT 0
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS prestamos (
                usuario_id INTEGER,
                libro_id INTEGER,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY(libro_id) REFERENCES libros(id)
            )
        ''')