from clase_libro_genero import generolibro

class Book:
    def __init__(self, titulo, autor, genero: generolibro):
        self._titulo = titulo
        self._autor = autor
        self._genero = genero
        self._is_prestado = False  # Estado de disponibilidad

    def get_titulo(self):
        return self._titulo

    def get_autor(self):
        return self._autor

    def get_genero(self):
        return self._genero

    def is_disponible(self):
        return not self._is_prestado  # Si no está prestado, está disponible

    # Métodos Setter
    def set_titulo(self, titulo):
        self._titulo = titulo

    def set_autor(self, autor):
        self._autor = autor

    def set_genero(self, genero: generolibro):
        self._genero = genero

    def prestar(self):
        if self.is_disponible():
            self._is_prestado = True
            return True
        return False

    def return_book(self):
        self._is_prestado = False
