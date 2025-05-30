import tkinter as tk
from tkinter import messagebox

class InterfazCombate:
    def __init__(self, master, jugador, ia):
        self.master = master
        self.jugador = jugador
        self.ia = ia
        master.title("Combate Pokemon")

        self.label_jugador = tk.Label(master, text=f"Tu Pokemon: {jugador.pokemon_activo}")
        self.label_jugador.pack()

        self.label_ia = tk.Label(master, text=f"Pokemon de la IA: {ia.pokemon_activo}")
        self.label_ia.pack()

        self.label_ps_jugador = tk.Label(master, text=f"Tu Pokemon PS: {jugador.pokemon_activo.ps}")
        self.label_ps_jugador.pack()

        self.label_ps_ia = tk.Label(master, text=f"Pokemon de la IA PS: {ia.pokemon_activo.ps}")
        self.label_ps_ia.pack()

        self.ataques_frame = tk.Frame(master)
        self.ataques_frame.pack()

        self.botones_ataques = []
        for ataque in jugador.pokemon_activo.ataques:
            boton = tk.Button(self.ataques_frame, text=ataque.nombre, command=lambda a=ataque.nombre: self.seleccionar_ataque(a))
            self.botones_ataques.append(boton)
            boton.pack(side=tk.LEFT)

        self.text_resultado = tk.Text(master, height=5, width=50)
        self.text_resultado.pack()

    def seleccionar_ataque(self, nombre_ataque):
        """Selecciona un ataque y actualiza la interfaz."""
        self.ataque_elegido = nombre_ataque
        self.master.destroy()  # Cerrar la ventana después de elegir el ataque

    def mostrar_resultado(self, ataque, danio, defensor_nombre):
        """Muestra el resultado del ataque en la interfaz."""
        resultado = f"Se usó el ataque {ataque.nombre} contra {defensor_nombre} y causó {danio:.2f} de daño.\n"
        self.text_resultado.insert(tk.END, resultado)
        self.text_resultado.see(tk.END)  # Autoscroll

    def mostrar_mensaje_fin_combate(self, ganador):
        """Muestra el mensaje de fin de combate."""
        messagebox.showinfo("Fin del combate", f"¡El ganador es {ganador}!")

    def actualizar_ps(self):
        """Actualiza las etiquetas de PS."""
        self.label_ps_jugador.config(text=f"Tu Pokemon PS: {self.jugador.pokemon_activo.ps:.2f}")
        self.label_ps_ia.config(text=f"Pokemon de la IA PS: {self.ia.pokemon_activo.ps:.2f}")

def leer_entrada_usuario(jugador, ia):
    """Crea una ventana Tkinter para que el usuario elija un ataque."""
    root = tk.Tk()
    interfaz = InterfazCombate(root, jugador, ia)
    root.mainloop()
    return interfaz.ataque_elegido

def mostrar_estado_actual(jugador, ia):
    """No es necesario en la interfaz gráfica."""
    pass
