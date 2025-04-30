# interfaz_gradio.py
import gradio as gr
from clase_empleado import Employee
from clase_usuario import User
from clase_libro_genero import generolibro
from clase_libros import Book
import sqlite3

empleado = Employee("Admin")
usuarios_creados = {}  # Almacenar instancias de usuarios en memoria

# Funciones conectadas a Gradio

def registrar_usuario(nombre):
    if nombre not in usuarios_creados:
        usuarios_creados[nombre] = User(nombre)
    return empleado.register_user(nombre)

def agregar_libro(titulo, autor, genero):
    try:
        genero_enum = generolibro[genero.upper()]
        return empleado.add_book(titulo, autor, genero_enum)
    except KeyError:
        return "❌ Género no válido."

def consultar_disponibilidad(titulo):
    return empleado.consultar_disponibilidad(titulo)

def realizar_prestamo(nombre_usuario, titulo_libro):
    if nombre_usuario not in usuarios_creados:
        usuarios_creados[nombre_usuario] = User(nombre_usuario)
    user = usuarios_creados[nombre_usuario]
    book = Book(titulo_libro, "", generolibro.FICTION)  # Autor y género no necesarios para préstamo
    return user.borrow_book(book)

def realizar_devolucion(nombre_usuario, titulo_libro):
    if nombre_usuario not in usuarios_creados:
        return "❌ Usuario no encontrado."
    user = usuarios_creados[nombre_usuario]
    book = Book(titulo_libro, "", generolibro.FICTION)
    # Verifica en la base de datos si ese usuario ha prestado ese libro
    with sqlite3.connect("biblioteca.db") as conn:
        c = conn.cursor()
        c.execute("SELECT u.id, l.id FROM usuarios u, libros l WHERE u.nombre = ? AND l.titulo = ?", (nombre_usuario, titulo_libro))
        resultado = c.fetchone()
        if not resultado:
            return "❌ Usuario o libro no encontrado."
        usuario_id, libro_id = resultado
        c.execute("SELECT * FROM prestamos WHERE usuario_id = ? AND libro_id = ?", (usuario_id, libro_id))
        prestamo = c.fetchone()
        if not prestamo:
            return "⚠️ El libro no fue prestado a este usuario."
    resultado = user.return_book(book)
    return resultado

# Interfaz Gradio
with gr.Blocks() as demo:
    gr.Markdown("# 📚 Sistema de Gestión de Biblioteca")

    with gr.Tab("Registrar Usuario"):
        nombre = gr.Textbox(label="Nombre del usuario")
        btn_registrar = gr.Button("Registrar")
        salida_registro = gr.Textbox(label="Resultado")
        btn_registrar.click(registrar_usuario, inputs=nombre, outputs=salida_registro)

    with gr.Tab("Agregar Libro"):
        titulo = gr.Textbox(label="Título del libro")
        autor = gr.Textbox(label="Autor")
        genero = gr.Textbox(label="Género (FICTION, NONFICTION, SCIENCE, ART, etc.)")
        btn_agregar = gr.Button("Agregar")
        salida_libro = gr.Textbox(label="Resultado")
        btn_agregar.click(agregar_libro, inputs=[titulo, autor, genero], outputs=salida_libro)

    with gr.Tab("Consultar Disponibilidad"):
        titulo_disp = gr.Textbox(label="Título del libro")
        btn_consultar = gr.Button("Consultar")
        resultado_disp = gr.Textbox(label="Estado")
        btn_consultar.click(consultar_disponibilidad, inputs=titulo_disp, outputs=resultado_disp)

    with gr.Tab("Realizar Préstamo"):
        nombre_usuario_p = gr.Textbox(label="Nombre del usuario")
        titulo_libro_p = gr.Textbox(label="Título del libro")
        btn_prestamo = gr.Button("Prestar")
        salida_prestamo = gr.Textbox(label="Resultado")
        btn_prestamo.click(realizar_prestamo, inputs=[nombre_usuario_p, titulo_libro_p], outputs=salida_prestamo)

    with gr.Tab("Realizar Devolución"):
        nombre_usuario_d = gr.Textbox(label="Nombre del usuario")
        titulo_libro_d = gr.Textbox(label="Título del libro")
        btn_devolucion = gr.Button("Devolver")
        salida_devolucion = gr.Textbox(label="Resultado")
        btn_devolucion.click(realizar_devolucion, inputs=[nombre_usuario_d, titulo_libro_d], outputs=salida_devolucion)

# Ejecutar interfaz
if __name__ == "__main__":
    demo.launch()
