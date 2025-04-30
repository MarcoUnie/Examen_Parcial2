from clase_libros import Book
from clase_libro_genero import generolibro
class User:
    def __init__(self, name):
        self._name = name
        self._borrow_history = []  # Historial de libros prestados

    def get_name(self):
        return self._name

    def get_history(self):
        return self._borrow_history

    def borrow_book(self, book: Book):
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
