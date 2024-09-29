import flet as ft
import webbrowser
import pyperclip
import threading
import time
from datetime import datetime
import pygame  # Usaremos pygame para el control del sonido
import json  # Para manejar la lectura y escritura en JSON
import os  # Para verificar si el archivo existe

# Archivo donde se guardarán las tareas
ARCHIVO_TAREAS = "tareas.json"

def main(page: ft.Page):
    # Inicializar pygame mixer para reproducir sonidos
    pygame.mixer.init()

    # Cargar las tareas desde el archivo JSON al inicio
    tareas = []

    def cargar_tareas():
        if os.path.exists(ARCHIVO_TAREAS):
            with open(ARCHIVO_TAREAS, "r") as archivo:
                return json.load(archivo)
        return []

    def guardar_tareas():
        with open(ARCHIVO_TAREAS, "w") as archivo:
            json.dump(tareas, archivo, indent=4)

    tareas = cargar_tareas()  # Cargar las tareas desde el archivo al iniciar

    tareas_columna = ft.Column(
        controls=[],
        alignment="start",
        spacing=10
    )

    def actualizar_lista_tareas():
        tareas_columna.controls.clear()
        if tareas:
            for tarea in tareas:
                tareas_columna.controls.append(
                    ft.ListTile(
                        title=ft.Text(tarea["Nombre"]),
                        subtitle=ft.Text(f"Inicia: {tarea['FechaInicio']} {tarea['HoraInicio']} - Fin: {tarea['FechaFin']} {tarea['HoraFin']}", size=12),
                        leading=ft.Icon(ft.icons.TASK),
                        trailing=ft.IconButton(
                            icon=ft.icons.DELETE,
                            icon_color="red",
                            on_click=lambda e, t=tarea: eliminar_tarea(t)
                        )
                    )
                )
        else:
            tareas_columna.controls.append(
                ft.Text("No hay tareas disponibles.", color="white")
            )
        page.update()

    def crear_tarea(e):
        if nombre_tarea_input.value:
            tarea = {
                "Nombre": nombre_tarea_input.value,
                "FechaInicio": fecha_inicio_input.value,
                "HoraInicio": hora_inicio_input.value,
                "FechaFin": fecha_fin_input.value,
                "HoraFin": hora_fin_input.value
            }
            tareas.append(tarea)
            guardar_tareas()  # Guardar en JSON al agregar una tarea
            nombre_tarea_input.value = ""
            fecha_inicio_input.value = ""
            hora_inicio_input.value = ""
            fecha_fin_input.value = ""
            hora_fin_input.value = ""
            actualizar_lista_tareas()
            cerrar_dialogo_tareas()

    def eliminar_tarea(tarea):
        tareas.remove(tarea)
        guardar_tareas()  # Guardar en JSON después de eliminar una tarea
        actualizar_lista_tareas()

    def abrir_dialogo_tareas(e):
        tareas_dialogo.open = True
        page.update()

    nombre_tarea_input = ft.TextField(
        hint_text="Escribe el nombre de la tarea",
        width=300,
        text_size=16
    )

    fecha_inicio_input = ft.TextField(hint_text="Fecha Inicio (YYYY-MM-DD)")
    hora_inicio_input = ft.TextField(hint_text="Hora Inicio (HH:MM)")
    fecha_fin_input = ft.TextField(hint_text="Fecha Fin (YYYY-MM-DD)")
    hora_fin_input = ft.TextField(hint_text="Hora Fin (HH:MM)")

    tareas_dialogo = ft.AlertDialog(
        title=ft.Text("Agregar Tarea"),
        content=ft.Column(
            [
                nombre_tarea_input,
                fecha_inicio_input,
                hora_inicio_input,
                fecha_fin_input,
                hora_fin_input,
            ],
            spacing=20,
            expand=True
        ),
        actions=[ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Cancelar", 
                    on_click=lambda e: cerrar_dialogo_tareas()
                ),
                ft.ElevatedButton(
                    text="Agregar",
                    bgcolor="#149E95",
                    color="white",
                    on_click=crear_tarea
                )
            ],
            alignment="center"
        )]
    )

    def cerrar_dialogo_tareas():
        tareas_dialogo.open = False
        page.update()

    # El resto del código permanece igual

    actualizar_lista_tareas()

    def mostrar_notificacion(tarea):
        def cerrar_notificacion(e):
            notificacion_dialogo.open = False
            page.update()
            pygame.mixer.music.stop()

        notificacion_dialogo = ft.AlertDialog(
            title=ft.Text("Notificación de Tarea"),
            content=ft.Text(f"La tarea '{tarea['Nombre']}' ha comenzado."),
            actions=[ft.ElevatedButton("Cerrar", on_click=cerrar_notificacion)]
        )
        notificacion_dialogo.open = True
        page.add(notificacion_dialogo)
        page.update()

        # Intentamos cargar y reproducir el sonido de notificación
        try:
            pygame.mixer.music.load('assets/notificacion.mp3')
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Error al reproducir el sonido: {e}")

    def notificar_tareas():
        while True:
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M")
            for tarea in tareas:
                tarea_inicio = f"{tarea['FechaInicio']} {tarea['HoraInicio']}"
                if tarea_inicio == current_time:
                    mostrar_notificacion(tarea)
            time.sleep(60)

    threading.Thread(target=notificar_tareas, daemon=True).start()

    def abrir_comentarios(e):
        webbrowser.open('mailto:chsolutionsoficial@gmail.com')

    def compartir_contenido(e):
        enlace = "https://chsolutionsoficial.github.io/"
        pyperclip.copy(enlace)
        print(f"Enlace copiado al portapapeles: {enlace}")
        webbrowser.open(enlace)
        print("Enlace abierto en el navegador.")

    def calificar(e):
        print("¡Califícanos clickeado!")

    def abrir_politicas(e):
        print("Políticas clickeado!")

    # Establecer el icono de la aplicación
    page.icon = "assets/icon.png"  # Cambia esta ruta por la ubicación de tu icono

    page.title = "TaskControl"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.scroll = "auto"
    page.bgcolor = "#011621"

    page.appbar = ft.AppBar(
        title=ft.Container(
            content=ft.Text("Tareas", size=20, color="#1B9E97", weight=ft.FontWeight.BOLD),
            margin=ft.margin.only(left=20)
        ),
        center_title=False,
        bgcolor="#001F33",
        actions=[
            ft.Container(
                ft.IconButton(
                    icon=ft.icons.SEARCH, 
                    icon_color="#1B9E97", 
                    on_click=lambda _: alternar_campo_busqueda()
                ),
                margin=ft.margin.only(right=20)
            )
        ]
    )

    campo_busqueda = ft.TextField(
        hint_text="Buscar tareas...",
        bgcolor="#001F33",
        color="#FFFFFF",
        border_color="#1B9E97",
        on_submit=lambda e: print(f"Búsqueda: {e.control.value}")
    )

    contenedor_busqueda = ft.Container(
        content=campo_busqueda,
        visible=False,
        padding=ft.padding.all(10),
        bgcolor="#001F33",
        border_radius=5
    )

    def alternar_campo_busqueda():
        contenedor_busqueda.visible = not contenedor_busqueda.visible
        page.update()

    def abrir_dialogo_acerca_de(e):
        dialogo_acerca_de.open = True
        page.update()

    dialogo_acerca_de = ft.AlertDialog(
        title=ft.Text("Acerca de", size=20),
        content=ft.Column(
            [
                ft.ListTile(
                    leading=ft.Icon(ft.icons.INFO, color="#FFFFFF"),
                    title=ft.Text("TaskControl: Beta-1.0.0", size=16, color="#FFFFFF", weight=ft.FontWeight.NORMAL)
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.COMMENT, color="#FFFFFF"),
                    title=ft.Text("Enviar Comentarios", size=16, color="#FFFFFF"),
                    on_click=abrir_comentarios,
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.SHARE, color="#FFFFFF"),
                    title=ft.Text("Compartir", size=16, color="#FFFFFF"),
                    on_click=compartir_contenido,
                ),
            ],
            spacing=10,
            expand=True
        ),
        actions=[ft.Row(
            controls=[
                ft.ElevatedButton("Cerrar", on_click=lambda e: cerrar_dialogo_acerca_de())
            ],
            alignment="center"
        )]
    )

    def cerrar_dialogo_acerca_de():
        dialogo_acerca_de.open = False
        page.update()

    def abrir_dialogo_agregar_tarea(e):
        abrir_dialogo_tareas(e)

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.ADD,
        bgcolor="#149E95",
        on_click=abrir_dialogo_agregar_tarea,
        offset=ft.Offset(0, -0.2),
    )
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    page.bottom_appbar = ft.BottomAppBar(
        bgcolor="#001F33",
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.CATEGORY, tooltip="Categorías", icon_color="#19958C", on_click=""),
                ft.IconButton(icon=ft.icons.ARTICLE, tooltip="Resumen", icon_color="#19958C"),
                ft.IconButton(icon=ft.icons.CALENDAR_MONTH, tooltip="Calendario", icon_color="#19958C"),
                ft.IconButton(icon=ft.icons.INFO, tooltip="Acerca de", icon_color="#19958C", on_click=abrir_dialogo_acerca_de),
            ],
            alignment="spaceEvenly"
        )
    )

    page.add(
        ft.Column(
            controls=[
                contenedor_busqueda,
                tareas_columna,
                dialogo_acerca_de,
                tareas_dialogo,
            ],
            alignment="spaceBetween",
            expand=True
        )
    )

ft.app(target=main)
