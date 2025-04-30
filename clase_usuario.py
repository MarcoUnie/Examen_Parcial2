from clase_libros import Book
from clase_libro_genero import generolibro
import sqlite3

class User:
    def __init__(self, name):
        self._name = name
        self._borrow_history = []

    def get_name(self):
        return self._name

    def get_history(self):
        return self._borrow_history

    def borrow_book(self, book: Book):
        with sqlite3.connect("biblioteca.db") as conn:
            c = conn.cursor()
            c.execute("SELECT id FROM usuarios WHERE nombre = ?", (self._name,))
            user = c.fetchone()
            c.execute("SELECT id, prestado FROM libros WHERE titulo = ?", (book.get_titulo(),))
            libro = c.fetchone()
            if not user:
                return "❌ Usuario no encontrado."
            elif not libro:
                return "❌ Libro no encontrado."
            elif libro[1] == 1:
                return "📕 Libro ya prestado."
            else:
                c.execute("INSERT INTO prestamos (usuario_id, libro_id) VALUES (?, ?)", (user[0], libro[0]))
                c.execute("UPDATE libros SET prestado = 1 WHERE id = ?", (libro[0],))
                self._borrow_history.append(book)
                print(f"{self._name} ha tomado prestado: {book.get_titulo()}")
                return "✅ Préstamo realizado."

    def return_book(self, book: Book):
        if book in self._borrow_history:
            with sqlite3.connect("biblioteca.db") as conn:
                c = conn.cursor()
                c.execute("SELECT id FROM libros WHERE titulo = ?", (book.get_titulo(),))
                libro = c.fetchone()
                c.execute("SELECT id FROM usuarios WHERE nombre = ?", (self._name,))
                user = c.fetchone()
                if libro and user:
                    c.execute("DELETE FROM prestamos WHERE usuario_id = ? AND libro_id = ?", (user[0], libro[0]))
                    c.execute("UPDATE libros SET prestado = 0 WHERE id = ?", (libro[0],))
                    self._borrow_history.remove(book)
                    print(f"{self._name} ha devuelto: {book.get_titulo()}")
                else:
                    print("No se pudo encontrar el libro o usuario para devolver.")
        else:
            print(f"{self._name} no tiene ese libro.")