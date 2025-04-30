import sqlite3
def crear_tablas():
    with sqlite3.connect("biblioteca.db") as conn:
        c = conn.cursor()

        # Crear tabla de usuarios
        c.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
        """)

        # Crear tabla de libros
        c.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            genero TEXT NOT NULL,
            prestado INTEGER DEFAULT 0
        )
        """)

        # Crear tabla de préstamos
        c.execute("""
        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            libro_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (libro_id) REFERENCES libros(id)
        )
        """)


if __name__ == "__main__":
    crear_tablas()