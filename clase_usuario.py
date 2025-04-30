import sqlite3
from clase_libros import Book

class User:
    def __init__(self, name):
        self._name = name
        self._borrow_history = []  # Historial de libros prestados

    def get_name(self):
        return self._name

    def get_history(self):
        return self._borrow_history

    def borrow_book(self, book: Book):
        with sqlite3.connect("biblioteca.db") as conn:
            c = conn.cursor()
            # Verifica si el usuario existe
            c.execute("SELECT id FROM usuarios WHERE nombre = ?", (self._name,))
            user = c.fetchone()
            # Verifica si el libro existe y está disponible
            c.execute("SELECT id, prestado FROM libros WHERE titulo = ?", (book.get_titulo(),))
            libro = c.fetchone()

            if not user:
                return "❌ Usuario no encontrado."
            elif not libro:
                return "❌ Libro no encontrado."
            elif libro[1] == 1:  # 1 significa que el libro está prestado
                return "📕 Libro ya prestado."
            else:
                # Realiza el préstamo y actualiza el estado del libro
                c.execute("INSERT INTO prestamos (usuario_id, libro_id) VALUES (?, ?)", (user[0], libro[0]))
                c.execute("UPDATE libros SET prestado = 1 WHERE id = ?", (libro[0],))
                self._borrow_history.append(book)  # Añadir el libro al historial del usuario
                return f"✅ Préstamo realizado: {book.get_titulo()}"

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
                self._borrow_history.append(book.get_titulo())  # Guarda solo el título
                return f"✅ Préstamo realizado: {book.get_titulo()}"

    def return_book(self, book: Book):
        titulo = book.get_titulo()
        if titulo in self._borrow_history:
            with sqlite3.connect("biblioteca.db") as conn:
                c = conn.cursor()
                c.execute("SELECT id FROM libros WHERE titulo = ?", (titulo,))
                libro = c.fetchone()
                c.execute("SELECT id FROM usuarios WHERE nombre = ?", (self._name,))
                user = c.fetchone()
                if libro and user:
                    c.execute("DELETE FROM prestamos WHERE usuario_id = ? AND libro_id = ?", (user[0], libro[0]))
                    c.execute("UPDATE libros SET prestado = 0 WHERE id = ?", (libro[0],))
                    self._borrow_history.remove(titulo)
                    return f"✅ Devolución realizada: {titulo}"
                else:
                    return "❌ No se encontró el libro o usuario."
        else:
            return f"⚠️ El libro '{titulo}' no fue prestado por este usuario."

