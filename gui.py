import tkinter as tk
from tkinter import messagebox
import random
from pokemon import Pokemon, Attack
from trainer import Trainer
from battle import Battle
from ai import AI

# Crear Pokémon
charmander = Pokemon("Charmander", "Fire", 100, [Attack("Scratch", "Normal", 40), Attack("Ember", "Fire", 50)])
squirtle = Pokemon("Squirtle", "Water", 100, [Attack("Tackle", "Normal", 40), Attack("Water Gun", "Water", 50)])
bulbasaur = Pokemon("Bulbasaur", "Grass", 100, [Attack("Tackle", "Normal", 40), Attack("Vine Whip", "Grass", 50)])
pikachu = Pokemon("Pikachu", "Electric", 100, [Attack("Quick Attack", "Normal", 40), Attack("Thunder Shock", "Electric", 50)])

pokemon_options = [charmander, squirtle, bulbasaur, pikachu]

# Función para seleccionar Pokémon
selected_pokemon = None
selected_ai_pokemon = None

all_types = ["Normal", "Fire", "Water", "Grass", "Electric"]

def ensure_complete_type_chart(chart):
    # Asegurar que todos los tipos estén definidos en cada clonación o simulación (para la IA también)
    for atk in all_types:
        if atk not in chart:
            chart[atk] = {}
        for defn in all_types:
            if defn not in chart[atk]:
                chart[atk][defn] = 1.0

    chart["Electric"]["Water"] = 2.0
    chart["Electric"]["Grass"] = 0.5
    chart["Electric"]["Electric"] = 0.5

    chart["Water"]["Electric"] = 0.5
    chart["Fire"]["Electric"] = 1.0
    chart["Grass"]["Electric"] = 1.0
    chart["Normal"]["Electric"] = 1.0
    for atk in all_types:
        if atk not in chart:
            chart[atk] = {}
        for defn in all_types:
            if defn not in chart[atk]:
                chart[atk][defn] = 1.0

    chart["Electric"]["Water"] = 2.0
    chart["Electric"]["Grass"] = 0.5
    chart["Electric"]["Electric"] = 0.5

    chart["Water"]["Electric"] = 0.5
    chart["Fire"]["Electric"] = 1.0
    chart["Grass"]["Electric"] = 1.0
    chart["Normal"]["Electric"] = 1.0

def start_battle():
    global all_types
    global selected_pokemon, selected_ai_pokemon, trainer1, trainer2, battle, ai

    if selected_pokemon is None:
        messagebox.showerror("Error", "Por favor selecciona un Pokémon")
        return

    selected_ai_pokemon = random.choice([p for p in pokemon_options if p != selected_pokemon])

    trainer1 = Trainer("Ash", [selected_pokemon])
    trainer2 = Trainer("AI", [selected_ai_pokemon])
    battle = Battle(trainer1, trainer2)

    ensure_complete_type_chart(battle.type_chart)

    ai = AI(depth=2)
    select_frame.pack_forget()
    create_battle_ui()
    update_ui()

# Interfaz de selección
root = tk.Tk()
root.title("Combate Pokémon")

select_frame = tk.Frame(root)
select_frame.pack(padx=10, pady=10)

tk.Label(select_frame, text="Selecciona tu Pokémon").pack(pady=5)

for pokemon in pokemon_options:
    btn = tk.Button(select_frame, text=str(pokemon), command=lambda p=pokemon: select_pokemon(p))
    btn.pack(pady=2)

def select_pokemon(pokemon):
    global selected_pokemon
    selected_pokemon = Pokemon(pokemon.name, pokemon.type, pokemon.max_hp, [Attack(a.name, a.type, a.power) for a in pokemon.attacks])
    start_battle()

# Combate UI
frame = tk.Frame(root)
status_label = tk.Label(frame, text="")
player_hp = tk.Label(frame, text="")
ai_hp = tk.Label(frame, text="")
attack_frame = tk.LabelFrame(frame, text="Ataques")
attack_buttons = []

def create_battle_ui():
    frame.pack(padx=10, pady=10)
    status_label.pack(pady=5)
    player_hp.pack()
    ai_hp.pack()
    attack_frame.pack(pady=10)
    for btn in attack_buttons:
        btn.destroy()
    attack_buttons.clear()

    current_attacks = battle.get_current_trainer().active_pokemon.attacks
    for i, attack in enumerate(current_attacks):
        btn = tk.Button(attack_frame, text=str(attack), width=25, command=lambda i=i: on_attack(i))
        btn.pack(pady=2)
        attack_buttons.append(btn)

def update_ui():
    status_label.config(text=f"Turno de {battle.get_current_trainer().name}")
    player_hp.config(text=f"{trainer1.active_pokemon.name} HP: {trainer1.active_pokemon.hp:.0f}/{trainer1.active_pokemon.max_hp}")
    ai_hp.config(text=f"{trainer2.active_pokemon.name} HP: {trainer2.active_pokemon.hp:.0f}/{trainer2.active_pokemon.max_hp}")

def disable_buttons():
    for btn in attack_buttons:
        btn.config(state=tk.DISABLED)

def enable_buttons():
    for btn in attack_buttons:
        btn.config(state=tk.NORMAL)

def on_attack(index):
    current_trainer = battle.get_current_trainer()
    opponent_trainer = battle.get_opponent_trainer()

    attack = current_trainer.choose_attack(index)
    damage = battle.perform_attack(attack, current_trainer.active_pokemon, opponent_trainer.active_pokemon)

    status = f"{current_trainer.active_pokemon.name} usó {attack.name} e hizo {damage:.0f} de daño."
    status_label.config(text=status)

    if battle.check_fainted(opponent_trainer.active_pokemon):
        status_label.config(text=status + f"\n{opponent_trainer.active_pokemon.name} se debilitó!")
        if not opponent_trainer.has_available_pokemon():
            messagebox.showinfo("Fin del combate", f"{current_trainer.name} gana el combate!")
            disable_buttons()
            return

    battle.switch_turn()
    update_ui()
    root.after(1000, ai_turn)

def ai_turn():
    if battle.get_current_trainer().name != "AI":
        return

    attack_index = ai.choose_best_attack(battle)
    attack = battle.get_current_trainer().choose_attack(attack_index)
    damage = battle.perform_attack(attack, battle.get_current_trainer().active_pokemon, battle.get_opponent_trainer().active_pokemon)

    status = f"{battle.get_current_trainer().active_pokemon.name} usó {attack.name} e hizo {damage:.0f} de daño."
    status_label.config(text=status)

    if battle.check_fainted(battle.get_opponent_trainer().active_pokemon):
        status_label.config(text=status + f"\n{battle.get_opponent_trainer().active_pokemon.name} se debilitó!")
        if not battle.get_opponent_trainer().has_available_pokemon():
            messagebox.showinfo("Fin del combate", f"{battle.get_current_trainer().name} gana el combate!")
            disable_buttons()
            return

    battle.switch_turn()
    update_ui()
    enable_buttons()

root.mainloop()
