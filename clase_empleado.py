from clase_libro_genero import generolibro
from clase_usuario import User
import sqlite3
class Employee:
    def __init__(self, name):
        self._name = name

    def register_user(self, name):
        print(f"Empleado {self._name} ha registrado al usuario: {name}")
        with sqlite3.connect("biblioteca.db") as conn:
            try:
                conn.execute("INSERT INTO usuarios (nombre) VALUES (?)", (name))
                return "👤 Usuario registrado."
            except sqlite3.IntegrityError:
                return "⚠️ El usuario ya existe."

        return User(name)

    def add_book(self, title, author, genre: generolibro):
        with sqlite3.connect("biblioteca.db") as conn:
            conn.execute("INSERT INTO libros (titulo, autor, genero) VALUES (?, ?, ?)", (title, author, genre))
            return "📘 Libro agregado."
        print(f"Empleado {self._name} ha agregado el libro: {title}")
        return Book(title, author, genre)

    def show_user_history(self, user: User):
        print(f"Historial de préstamos de {user.get_name()}:")
        for book in user.get_history():
            print(f"- {book.get_titulo()} por {book.get_autor()}")
