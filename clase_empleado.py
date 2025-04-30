# clase_empleado.py
import sqlite3
from clase_libro_genero import generolibro
class Employee:
    def __init__(self, name):
        self._name = name

    def register_user(self, name):
        with sqlite3.connect("biblioteca.db") as conn:
            try:
                conn.execute("INSERT INTO usuarios (nombre) VALUES (?)", (name,))
                return f"👤 Usuario '{name}' registrado por {self._name}."
            except sqlite3.IntegrityError:
                return f"⚠️ El usuario '{name}' ya existe."

    def add_book(self, title, author, genre: generolibro):
        with sqlite3.connect("biblioteca.db") as conn:
            try:
                conn.execute(
                    "INSERT INTO libros (titulo, autor, genero, prestado) VALUES (?, ?, ?, 0)",
                    (title, author, genre.name),
                )
                return f"📘 Libro '{title}' agregado por {self._name}."
            except sqlite3.IntegrityError:
                return f"⚠️ El libro '{title}' ya existe."

    def consultar_disponibilidad(self, titulo_libro):
        with sqlite3.connect("biblioteca.db") as conn:
            c = conn.cursor()
            c.execute("SELECT prestado FROM libros WHERE titulo = ?", (titulo_libro,))
            result = c.fetchone()
            if result is None:
                return "❌ Libro no encontrado."
            return "✅ Disponible" if result[0] == 0 else "❌ Prestado"

    def show_user_history(self, user_name):
        with sqlite3.connect("biblioteca.db") as conn:
            c = conn.cursor()
            c.execute("""
                SELECT libros.titulo, libros.autor 
                FROM prestamos
                JOIN usuarios ON prestamos.usuario_id = usuarios.id
                JOIN libros ON prestamos.libro_id = libros.id
                WHERE usuarios.nombre = ?
            """, (user_name,))
            libros = c.fetchall()
            if not libros:
                return f"📭 No hay historial de préstamos para {user_name}."
            historial = f"📚 Historial de préstamos de {user_name}:\n"
            for titulo, autor in libros:
                historial += f"- {titulo} por {autor}\n"
            return historial.strip()
