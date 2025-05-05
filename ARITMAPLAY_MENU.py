import tkinter as tk 
import subprocess
import sys
import pygame
import subprocess
import os

# Colores y fuentes
FONDO = "#1e1e2f"
BOTON_COLOR = "#4e88ff"
TEXTO_COLOR = "#ffffff"
FUENTE_TITULO = ("Comic Sans MS", 20, "bold")
FUENTE_BOTON = ("Verdana", 12, "bold")

# Inicializar pygame mixer
pygame.mixer.init()
pygame.mixer.music.load("musiquita.wav")  # Asegúrate de tener este archivo en la misma carpeta
pygame.mixer.music.play(-1)  # -1 para que se repita en bucle



def iniciar_aritmaplay():
    pygame.mixer.music.stop()  # Detener la música al iniciar el juego
    ventana.destroy()
    subprocess.Popen([os.path.join(os.getcwd(), "prueba.exe")])  # Ejecuta el juego

def mostrar_creditos():
    creditos_ventana = tk.Toplevel(ventana)
    creditos_ventana.title("Créditos")
    creditos_ventana.geometry("500x400")
    creditos_ventana.resizable(False, False)
    creditos_ventana.config(bg="#f4f4f4")

    titulo_creditos = tk.Label(
        creditos_ventana, text="Créditos",
        font=("Arial", 24, "bold"), fg="#4B0082", bg="#f4f4f4"
    )
    titulo_creditos.pack(pady=20)

    creditos_texto = """
Integrantes del grupo:
-------------------------
CORREA VACA SANTIAGO
NAIDA STEFANY JIMÉNEZ GONZALES
CLARITA VERONICA FRÍAS HURTADO
JANNETH YHAMARA NAVIA BALDELOMAR

Agradecimientos a:
-------------------
- Nuestra Licenciada Ligia Marcela Baspineiro Zabala
- Herramientas utilizadas: Python, Tkinter, Pygame

¡Gracias por jugar y apoyar el proyecto!
"""

    creditos_box = tk.Text(
        creditos_ventana, font=("Arial", 12), fg="#333333", bg="#f4f4f4",
        wrap="word", padx=20, pady=20, height=10, width=50
    )
    creditos_box.insert(tk.END, creditos_texto)
    creditos_box.config(state=tk.DISABLED)
    creditos_box.pack(pady=10)

    boton_cerrar = tk.Button(
        creditos_ventana, text="Cerrar", font=("Arial", 14, "bold"),
        bg="#32CD32", fg="white", command=creditos_ventana.destroy,
        bd=0, relief="flat", cursor="hand2"
    )
    boton_cerrar.pack(pady=10)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("AritmaPlay - Menú")
ventana.geometry("400x300")
ventana.configure(bg=FONDO)
ventana.resizable(False, False)

# Centrar la ventana
ancho = 400
alto = 300
pantalla_ancho = ventana.winfo_screenwidth()
pantalla_alto = ventana.winfo_screenheight()
x = (pantalla_ancho // 2) - (ancho // 2)
y = (pantalla_alto // 2) - (alto // 2)
ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# Título del juego
titulo = tk.Label(
    ventana, text="¡Bienvenido a AritmaPlay!",
    font=FUENTE_TITULO, bg=FONDO, fg=TEXTO_COLOR
)
titulo.pack(pady=20)

# Botón Jugar
btn_jugar = tk.Button(
    ventana, text="JUGAR", font=FUENTE_BOTON, bg=BOTON_COLOR, fg=TEXTO_COLOR,
    activebackground="#355fb3", activeforeground=TEXTO_COLOR,
    relief="flat", width=15, height=2, command=iniciar_aritmaplay
)
btn_jugar.pack(pady=5)

# Botón Créditos
btn_creditos = tk.Button(
    ventana, text="CRÉDITOS", font=FUENTE_BOTON, bg="#ffa500", fg=TEXTO_COLOR,
    activebackground="#cc8400", activeforeground=TEXTO_COLOR,
    relief="flat", width=15, height=2, command=mostrar_creditos
)
btn_creditos.pack(pady=5)

# Botón Salir
btn_salir = tk.Button(
    ventana, text="SALIR", font=FUENTE_BOTON, bg="#ff4e4e", fg=TEXTO_COLOR,
    activebackground="#b33535", activeforeground=TEXTO_COLOR,
    relief="flat", width=15, height=2, command=lambda: (pygame.mixer.music.stop(), ventana.destroy())
)
btn_salir.pack(pady=5)

ventana.mainloop()
