# gui.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from trainer import Trainer
from battle import Battle, Attack
from ai import AI
import random
from tkinter import ttk

class PokemonBattleGUI:
    def __init__(self, all_pokemons):
        self.all_pokemons = all_pokemons
        self.selected_player_pokemons = []
        self.selected_ai_pokemons = random.sample([p for p in all_pokemons], 3)
        self.window = tk.Tk()
        self.window.title("Pokemon Battle")
        self.trainer1 = None
        self.trainer2 = None
        self.battle = None
        self.ai = None
        self.current_attack_buttons = []
        self.image_labels = []
        
        # Configurar la pantalla de selección
        self.setup_selection_screen()

    def setup_selection_screen(self):
        # Limpiar todos los widgets actuales
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Crear un frame principal
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear un label para indicar que se debe seleccionar un Pokémon
        tk.Label(main_frame, text="Selecciona 3 Pokémon:", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Crear el contador de selección
        self.selection_status = tk.Label(main_frame, text="Seleccionados: 0/3", font=("Arial", 12))
        self.selection_status.pack(pady=10)
        
        # Crear un frame para la cuadrícula
        grid_frame = tk.Frame(main_frame)
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Organizar los Pokémon en una cuadrícula
        row = 0
        col = 0
        for pokemon in self.all_pokemons:
            # Crear un frame para cada Pokémon
            pokemon_frame = tk.Frame(grid_frame, borderwidth=2, relief="solid", padx=5, pady=5)
            pokemon_frame.grid(row=row, column=col, padx=5, pady=5)
            
            # Cargar y mostrar la imagen del Pokémon
            try:
                img = Image.open(pokemon['image_path'])
                img = img.resize((80, 80))
                img = ImageTk.PhotoImage(img)
                label = tk.Label(pokemon_frame, image=img)
                label.image = img
                label.pack()
            except Exception as e:
                print(f"Error al cargar imagen de {pokemon['name']}: {e}")
            
            # Mostrar nombre y tipo
            name_label = tk.Label(pokemon_frame, text=f"{pokemon['name']}\n{pokemon['type']}")
            name_label.pack()
            
            # Botón de selección
            btn = tk.Button(pokemon_frame, text="Seleccionar", command=lambda p=pokemon: self.select_pokemon(p))
            btn.pack()
            
            # Actualizar posición para la siguiente columna
            col += 1
            if col >= 6:  # 6 Pokémon por fila
                col = 0
                row += 1
        
        # Ajustar el tamaño de la ventana
        self.window.geometry("800x600")
        
        # Centrar la ventana en la pantalla
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def select_pokemon(self, pokemon):
        if pokemon in self.selected_ai_pokemons:
            return  # No permitir seleccionar Pokémon de la IA
            
        if pokemon in self.selected_player_pokemons:
            self.selected_player_pokemons.remove(pokemon)
        else:
            if len(self.selected_player_pokemons) < 3:
                self.selected_player_pokemons.append(pokemon)
        
        # Actualizar el contador
        self.selection_status.config(text=f"Seleccionados: {len(self.selected_player_pokemons)}/3")
        
        # Iniciar la batalla si se han seleccionado 3 Pokémon
        if len(self.selected_player_pokemons) == 3:
            self.start_battle()

    def start_battle(self):
        # Limpiar todos los widgets actuales
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Crear un frame principal con scroll
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear un canvas con scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar el canvas y el scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Crear un frame para el registro de batalla
        self.battle_log = tk.Text(scrollable_frame, height=10, width=50)
        self.battle_log.pack(pady=10)
        
        # Crear un frame para los Pokémon
        pokemon_frame = tk.Frame(scrollable_frame)
        pokemon_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para el Pokémon del jugador
        player_frame = tk.Frame(pokemon_frame)
        player_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame para el Pokémon de la IA
        ai_frame = tk.Frame(pokemon_frame)
        ai_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Mostrar el Pokémon actual del jugador
        self.player_pokemon = self.selected_player_pokemons[0]
        self.player_image = Image.open(self.player_pokemon['image_path'])
        self.player_image = self.player_image.resize((200, 200))
        self.player_image = ImageTk.PhotoImage(self.player_image)
        self.player_label = tk.Label(player_frame, image=self.player_image)
        self.player_label.pack()
        
        # Mostrar el nombre y HP del Pokémon del jugador
        self.player_info = tk.Label(player_frame, text=f"{self.player_pokemon['name']}\nHP: {self.player_pokemon['hp']}")
        self.player_info.pack()
        
        # Mostrar el Pokémon actual de la IA
        self.ai_pokemon = self.selected_ai_pokemons[0]
        self.ai_image = Image.open(self.ai_pokemon['image_path'])
        self.ai_image = self.ai_image.resize((200, 200))
        self.ai_image = ImageTk.PhotoImage(self.ai_image)
        self.ai_label = tk.Label(ai_frame, image=self.ai_image)
        self.ai_label.pack()
        
        # Mostrar el nombre y HP del Pokémon de la IA
        self.ai_info = tk.Label(ai_frame, text=f"{self.ai_pokemon['name']}\nHP: {self.ai_pokemon['hp']}")
        self.ai_info.pack()
        
        # Crear un frame para los ataques
        attacks_frame = tk.Frame(scrollable_frame)
        attacks_frame.pack(pady=10)
        
        # Crear botones para cada ataque
        for i, attack in enumerate(self.player_pokemon['attacks']):
            btn = tk.Button(attacks_frame, text=attack.name, command=lambda a=attack: self.use_attack(a))
            btn.grid(row=0, column=i, padx=5)
        
        # Crear la instancia de Battle
        self.battle = Battle(self.player_pokemon, self.ai_pokemon)
        
        # Ajustar el tamaño de la ventana
        self.window.geometry("800x600")
        
        # Centrar la ventana en la pantalla
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def use_attack(self, attack):
        # Ejecutar el ataque a través de la clase Battle
        result = self.battle.execute_turn(attack)
        
        # Actualizar la interfaz según el resultado
        if result['player_attack']:
            self.battle_log.insert(tk.END, f"{self.player_pokemon['name']} usó {attack.name} y causó {result['player_damage']} de daño a {self.ai_pokemon['name']}\n")
            self.ai_info.config(text=f"{self.ai_pokemon['name']}\nHP: {max(0, self.ai_pokemon['hp'])}")
        
        if result['ai_attack']:
            self.battle_log.insert(tk.END, f"{self.ai_pokemon['name']} usó {result['ai_attack'].name} y causó {result['ai_damage']} de daño a {self.player_pokemon['name']}\n")
            self.player_info.config(text=f"{self.player_pokemon['name']}\nHP: {max(0, self.player_pokemon['hp'])}")
        
        self.battle_log.see(tk.END)
        
        # Verificar si algún Pokémon ha muerto
        if result['ai_fainted']:
            self.battle_log.insert(tk.END, f"{self.ai_pokemon['name']} ha sido derrotado\n")
            self.battle_log.see(tk.END)
            
            # Verificar si la IA se quedó sin Pokémon
            if len(self.selected_ai_pokemons) <= 1:
                self.battle_log.insert(tk.END, "¡Has ganado la batalla!\n")
                self.battle_log.see(tk.END)
                # Cerrar el juego después de 2 segundos
                self.window.after(2000, lambda: self.window.destroy())
                return
            
            # Eliminar el Pokémon derrotado de la lista
            self.selected_ai_pokemons.pop(0)
            
            # Actualizar el Pokémon de la IA
            self.ai_pokemon = self.selected_ai_pokemons[0]
            self.ai_image = Image.open(self.ai_pokemon['image_path'])
            self.ai_image = self.ai_image.resize((200, 200))
            self.ai_image = ImageTk.PhotoImage(self.ai_image)
            self.ai_label.config(image=self.ai_image)
            self.ai_info.config(text=f"{self.ai_pokemon['name']}\nHP: {self.ai_pokemon['hp']}")
            
            # Actualizar la instancia de Battle
            self.battle = Battle(self.player_pokemon, self.ai_pokemon)
        
        if result['player_fainted']:
            self.battle_log.insert(tk.END, f"{self.player_pokemon['name']} ha sido derrotado\n")
            self.battle_log.see(tk.END)
            
            # Verificar si el jugador se quedó sin Pokémon
            if len(self.selected_player_pokemons) <= 1:
                self.battle_log.insert(tk.END, "¡Has perdido la batalla!\n")
                self.battle_log.see(tk.END)
                # Cerrar el juego después de 2 segundos
                self.window.after(2000, lambda: self.window.destroy())
                return
            
            # Eliminar el Pokémon derrotado de la lista
            self.selected_player_pokemons.pop(0)
            
            # Mostrar la pantalla de selección de Pokémon
            self.show_pokemon_selection()

    def select_battle_pokemon(self, pokemon):
        # Seleccionar el nuevo Pokémon
        self.player_pokemon = pokemon
        
        # Volver a la batalla
        self.start_battle()
        
        # Añadir mensaje al registro de batalla
        self.battle_log.insert(tk.END, f"Has cambiado a {pokemon['name']}\n")
        self.battle_log.see(tk.END)
        
        # Actualizar la instancia de Battle con el nuevo Pokémon
        self.battle = Battle(self.player_pokemon, self.ai_pokemon)

    def show_pokemon_selection(self):
        # Limpiar todos los widgets actuales
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Crear un frame principal
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear un título
        title = tk.Label(main_frame, text="Selecciona tu siguiente Pokémon", font=("Arial", 16))
        title.pack(pady=20)
        
        # Crear un frame para los Pokémon
        pokemon_frame = tk.Frame(main_frame)
        pokemon_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Mostrar los Pokémon disponibles
        for i, pokemon in enumerate(self.selected_player_pokemons):
            # Crear un frame para cada Pokémon
            pokemon_container = tk.Frame(pokemon_frame)
            pokemon_container.grid(row=0, column=i, padx=10)
            
            # Mostrar la imagen del Pokémon
            image = Image.open(pokemon['image_path'])
            image = image.resize((150, 150))
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(pokemon_container, image=photo)
            label.image = photo  # Mantener una referencia
            label.pack()
            
            # Mostrar el nombre y HP del Pokémon
            info = tk.Label(pokemon_container, text=f"{pokemon['name']}\nHP: {pokemon['hp']}")
            info.pack()
            
            # Crear un botón para seleccionar el Pokémon
            btn = tk.Button(pokemon_container, text="Seleccionar", 
                          command=lambda p=pokemon: self.select_battle_pokemon(p))
            btn.pack()
        
        # Ajustar el tamaño de la ventana
        self.window.geometry("800x400")
        
        # Centrar la ventana en la pantalla
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def check_battle_state(self, msg, player_turn):
        if self.battle.battle_over():
            winner = self.battle.get_winner()
            messagebox.showinfo("Game Over", f"{winner.name} wins!")
            self.window.quit()
            return

        self.update_battle_screen()

    def run(self):
        self.window.mainloop()
