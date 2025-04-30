from clase_libros import Book
from clase_libro_genero import generolibro
import sqlite3
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
            c.execute("SELECT id FROM usuarios WHERE nombre = ?", (nombre_usuario,))
            user = c.fetchone()
            c.execute("SELECT id, prestado FROM libros WHERE titulo = ?", (titulo_libro,))
            book = c.fetchone()
            if not user:
                return "❌ Usuario no encontrado."
            elif not book:
                return "❌ Libro no encontrado."
            elif book[1] == 1:
                return "📕 Libro ya prestado."
            else:
                c.execute("INSERT INTO prestamos (usuario_id, libro_id) VALUES (?, ?)", (user[0], book[0]))
                c.execute("UPDATE libros SET prestado = 1 WHERE id = ?", (book[0],))
                return "✅ Préstamo realizado."
        if book.prestado():
            self._borrow_history.append(book)
            print(f"{self._name} ha tomado prestado: {book.get_titulo()}")
        else:
            print(f"{book.get_titulo()} no está disponible para préstamo.")

    def return_book(self, book: Book):
        if book in self._borrow_history:
            book.return_book()
            print(f"{self._name} ha devuelto: {book.get_titulo()}")
        else:
            print(f"{self._name} no tiene ese libro.")
