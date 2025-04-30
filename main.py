# interfaz_gradio.py
import gradio as gr
from clase_empleado import Employee
from clase_usuario import User
from clase_libro_genero import generolibro
from clase_libros import Book

empleado = Employee("Admin")

# Funciones conectadas a Gradio

def registrar_usuario(nombre):
    return empleado.register_user(nombre)

def agregar_libro(titulo, autor, genero):
    try:
        genero_enum = generolibro[genero.upper()]
        return empleado.add_book(titulo, autor, genero_enum)
    except KeyError:
        return "❌ Género no válido."

def consultar_disponibilidad(titulo):
    return empleado.consultar_disponibilidad(titulo)

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

# Ejecutar interfaz
if __name__ == "__main__":
    demo.launch()
