from clase_libro_genero import generolibro
from clase_usuario import User
from clase_libros import Book
import sqlite3

class Employee:
    def __init__(self, name):
        self._name = name

    def register_user(self, name):
        print(f"Empleado {self._name} ha registrado al usuario: {name}")
        with sqlite3.connect("biblioteca.db") as conn:
            try:
                conn.execute("INSERT INTO usuarios (nombre) VALUES (?)", (name,))
                return "👤 Usuario registrado."
            except sqlite3.IntegrityError:
                return "⚠️ El usuario ya existe."

    def add_book(self, title, author, genre: generolibro):
        with sqlite3.connect("biblioteca.db") as conn:
            conn.execute("INSERT INTO libros (titulo, autor, genero) VALUES (?, ?, ?)", (title, author, genre.value))
            print(f"Empleado {self._name} ha agregado el libro: {title}")
            return "📘 Libro agregado."

    def show_user_history(self, user: User,book: Book):
        with sqlite3.connect("biblioteca.db") as conn:
            c = conn.cursor()
            c.execute("SELECT id FROM usuarios WHERE nombre = ?", (user,))
            user = c.fetchone()
            if not user:
                return "❌ Usuario no encontrado."
            c.execute('''
                SELECT libros.titulo FROM prestamos
                JOIN libros ON prestamos.libro_id = libros.id
                WHERE prestamos.usuario_id = ?
            ''', (user[0],))
            libros = [f"- {row[0]}" for row in c.fetchall()]
            return "\n".join(libros) if libros else "📭 sin prestamos activos"
        print(f"Historial de préstamos de {user.get_name()}:")
        for book in user.get_history():
            print(f"- {book.get_titulo()} por {book.get_autor()}")

    def consultar_disponibilidad(self, titulo_libro):
        with sqlite3.connect("biblioteca.db") as conn:
            c = conn.cursor()
            c.execute("SELECT prestado FROM libros WHERE titulo = ?", (titulo_libro,))
            result = c.fetchone()
            if result is None:
                return "❌ Libro no encontrado."
            return "Disponible ✅" if result[0] == 0 else "Prestado ❌"

