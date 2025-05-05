import tkinter as tk
import random
from tkinter import messagebox
from PIL import Image, ImageTk
def generar_posiciones_separadas(cantidad, min_distancia=80):
    posiciones = []
    intentos_maximos = 1000
    intentos = 0
    while len(posiciones) < cantidad and intentos < intentos_maximos:
        intentos += 1
        x = random.randint(50, 500)
        y = random.randint(400, 550)
        valida = True
        for (px, py) in posiciones:
            distancia = ((x - px) ** 2 + (y - py) ** 2) ** 0.5
            if distancia < min_distancia:
                valida = False
                break
        if valida:
            posiciones.append((x, y))
    return posiciones

def mostrar_ejercicio(globo):
    global resultado_correcto, globo_seleccionado, tiempo_respuesta

    tipo = random.choice(['simple', 'multiplicacion_grande', 'division', 'combinada', 'parentesis'])

    if tipo == 'simple':
        operador = random.choice(['+', '-'])
        num1 = random.randint(10, 99)
        num2 = random.randint(10, 99)
        if operador == '-' and num1 < num2:
            num1, num2 = num2, num1
        ejercicio = f"{num1} {operador} {num2}"

    elif tipo == 'multiplicacion_grande':
        num1 = random.randint(10, 20)
        num2 = random.randint(10, 20)
        ejercicio = f"{num1} * {num2}"

    elif tipo == 'division':
        num2 = random.randint(2, 10)
        resultado = random.randint(2, 10)
        num1 = num2 * resultado
        ejercicio = f"{num1} / {num2}"

    elif tipo == 'combinada':
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        c = random.randint(1, 10)
        ejercicio = f"{a} + {b} * {c}"

    elif tipo == 'parentesis':
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        c = random.randint(1, 10)
        ejercicio = f"({a} + {b}) * {c}"

    resultado_correcto = eval(ejercicio)
    etiqueta_ejercicio.config(text=f"{ejercicio} = ?")
    entrada_respuesta.delete(0, tk.END)
    globo_seleccionado = globo


def verificar_respuesta():
    global puntuacion, vidas, globo_seleccionado, temporizador_activo, temporizador_id

    try:
        respuesta = int(entrada_respuesta.get())
        if respuesta == resultado_correcto:
            etiqueta_resultado.config(text="✅ ¡Correcto!", fg="#27ae60")
            puntuacion += 1
        else:
            etiqueta_resultado.config(text=f"❌ Incorrecto. Era {resultado_correcto}", fg="#e74c3c")
            puntuacion = max(0, puntuacion - 1)
            vidas -= 1
            corazones[vidas].config(text="🤍")
            if vidas == 0:
                etiqueta_resultado.config(text="💀 Se acabó el juego. ¡Perdiste!", fg="black")
                for globo in globos:
                    globo.place_forget()
                ventana.after(2000, mostrar_opciones_finales)
                return

        if globo_seleccionado:
            globo_seleccionado.place_forget()
            globos.remove(globo_seleccionado)
            globo_seleccionado = None

        etiqueta_puntaje.config(text=f"Puntaje: {puntuacion}")

        if not globos:
            # Detener temporizador si está activo
            if temporizador_id is not None:
                ventana.after_cancel(temporizador_id)
                temporizador_id = None
                temporizador_activo = False

            mostrar_animacion_felicitaciones()
            ventana.after(1000, lambda: messagebox.showinfo("¡Felicidades!", "🎉 ¡Has completado todos los ejercicios correctamente! 🎉"))
            ventana.after(3000, mostrar_opciones_finales)
            return

        reposicionar_globos()
        etiqueta_ejercicio.config(text="")
        ventana.after(1500, lambda: etiqueta_resultado.config(text=""))
        entrada_respuesta.delete(0, tk.END)

    except:
        etiqueta_resultado.config(text="❗ Ingresa un número válido", fg="orange")


    




    
# Función que muestra el mensaje cuando el jugador pierde o el tiempo se agota
def mostrar_opciones_finales():
    respuesta = messagebox.askyesno("Juego terminado", "¿Quieres reiniciar el juego?")
    if respuesta:
        reiniciar_juego()  # Asegúrate de tener esta función definida en algún lugar de tu código
    else:
        ventana.quit()  # Cierra la ventana del juego


def reposicionar_globos():
    posiciones = generar_posiciones_separadas(len(globos))
    for globo, (x, y) in zip(globos, posiciones):
        globo.place(x=x, y=y)

def animar_globos():
    for globo in globos:
        x = globo.winfo_x()
        y = globo.winfo_y()
        if y > 420:
            globo.place(x=x, y=y - 1)
    ventana.after(50, animar_globos)

def contar_tiempo():
    global tiempo_respuesta, temporizador_activo, temporizador_id

    if not temporizador_activo:
        temporizador_activo = True

    if tiempo_respuesta > 0:
        etiqueta_tiempo.config(text=f"Tiempo: {tiempo_respuesta}s")
        tiempo_respuesta -= 1
        temporizador_id = ventana.after(1000, contar_tiempo)  # Guardamos el ID
    else:
        etiqueta_resultado.config(text="⏳ ¡Tiempo agotado!", fg="orange")
        for globo in globos:
            globo.place_forget()
        entrada_respuesta.config(state="disabled")
        temporizador_activo = False
        ventana.after(2000, mostrar_opciones_finales)  # Mostrar opciones después de 2 segundos


def mostrar_animacion_felicitaciones():
    confetis = []

    def animar_confeti():
        for emoji in confetis:
            y = emoji.winfo_y()
            if y < 700:
                emoji.place(y=y + 5)
            else:
                emoji.destroy()
                confetis.remove(emoji)
        if confetis:
            ventana.after(50, animar_confeti)

    for _ in range(15):
        x = random.randint(0, 550)
        emoji = tk.Label(ventana, text=random.choice(["🎉", "✨", "🎊", "🌟"]), font=("Arial", 20), bg="#ADD8E6")
        emoji.place(x=x, y=0)
        confetis.append(emoji)

    animar_confeti()


def reiniciar_juego():
    global vidas, puntuacion, tiempo_respuesta, globos, globo_seleccionado, temporizador_activo, temporizador_id
    # Cancelar temporizador anterior si existe
    if temporizador_id is not None:
        ventana.after_cancel(temporizador_id)
        temporizador_id = None
        temporizador_activo = False

    # El resto del reinicio como lo tengas implementado

    # Reiniciar variables
    vidas = 3
    puntuacion = 0
    tiempo_respuesta = 30
    temporizador_activo = False
    globo_seleccionado = None

    # 💡 Asegúrate de eliminar todos los globos viejos de la interfaz
    for globo in globos:
        globo.destroy()
    globos.clear()

    # Restaurar corazones
    for lbl in corazones:
        lbl.config(text="❤️")

    # Restaurar etiquetas
    etiqueta_puntaje.config(text="Puntaje: 0")
    
    etiqueta_resultado.config(text="")
    etiqueta_ejercicio.config(text="")
    entrada_respuesta.config(state="normal")
    entrada_respuesta.delete(0, tk.END)

    # Crear nuevos globos
    posiciones = generar_posiciones_separadas(3)
    for i in range(3):  # 👈 Asegúrate que sean exactamente 3
        x, y = posiciones[i]
        color = random.choice(["#ff2d00"])
        globo = tk.Button(
            ventana,
            text="🎈",
            font=("Arial", 24),
            bg=color,
            command=lambda g=None: mostrar_ejercicio(g),
            borderwidth=0,
            activebackground=color
        )
        globo.config(command=lambda g=globo: mostrar_ejercicio(g))
        globo.place(x=x, y=y)
        globos.append(globo)

    # Reiniciar temporizador y animación
    contar_tiempo()
    animar_globos()


# Ventana principal
ventana = tk.Tk()
ventana.title("🎈 Juego de los Globos Aritméticos")
ventana.geometry("600x700")
ventana.config(bg="#ADD8E6")  # Azul cielo claro
fondo_imagen = Image.open("h.jpg")
fondo_tk = ImageTk.PhotoImage(fondo_imagen)
fondo_label = tk.Label(ventana, image=fondo_tk)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
fondo_label.lower()


nivel = 1
tiempo_respuesta = 30
max_nivel = 5
puntuacion = 0
vidas = 3
resultado_correcto = 0
globos = []
globo_seleccionado = None
temporizador_activo = False
temporizador_id = None  # al principio del código


# Estilo general
fuente_titulo = ("Comic Sans MS", 20, "bold")
fuente_normal = ("Comic Sans MS", 16)

etiqueta_ejercicio = tk.Label(ventana, text="", font=fuente_titulo, bg="#ADD8E6")
etiqueta_ejercicio.pack(pady=10)

entrada_respuesta = tk.Entry(ventana, font=("Comic Sans MS", 18), justify="center", width=10)
entrada_respuesta.pack(pady=5)

boton_verificar = tk.Button(ventana, text="Verificar", command=verificar_respuesta, font=fuente_normal, bg="#2980b9", fg="white", relief="raised", width=12)
boton_verificar.pack(pady=10)

etiqueta_resultado = tk.Label(ventana, text="", font=fuente_normal, bg="#ADD8E6")
etiqueta_resultado.pack()

etiqueta_puntaje = tk.Label(ventana, text="Puntaje: 0", font=fuente_normal, bg="#ADD8E6")
etiqueta_puntaje.pack(pady=10)

etiqueta_tiempo = tk.Label(ventana, text="Tiempo: 30s", font=fuente_normal, bg="#ADD8E6")
etiqueta_tiempo.pack(pady=5)


# Corazones
corazones = []
marco_corazones = tk.Frame(ventana, bg="#ADD8E6")
marco_corazones.pack(pady=5)
for _ in range(3):
    lbl = tk.Label(marco_corazones, text="❤️", font=("Comic Sans MS", 24), bg="#ADD8E6")
    lbl.pack(side="left", padx=5)
    corazones.append(lbl)

# Crear globos
posiciones = generar_posiciones_separadas(3)
for i in range(3):
    x, y = posiciones[i]
    color = random.choice(["#c500ff"])
    globo = tk.Button(
        ventana,
        text="🎈",
        font=("Arial", 24),
        bg=color,
        command=lambda g=None: mostrar_ejercicio(g),
        borderwidth=0,
        activebackground=color
    )
    globo.config(command=lambda g=globo: mostrar_ejercicio(g))
    globo.place(x=x, y=y)
    globos.append(globo)

if not temporizador_activo:
    contar_tiempo()

animar_globos()


ventana.mainloop()
