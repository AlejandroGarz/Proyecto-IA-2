# main.py
import pandas as pd
import random
from battle import Attack
from trainer import Trainer
from battle import Battle
from ai import AI
from gui import PokemonBattleGUI

def load_data_from_excel(filename):
    df_pokemon = pd.read_excel(filename, sheet_name='Sheet1')
    
    df_attacks = pd.read_excel(filename, sheet_name='Sheet1')

    attacks_dict = {}
    for i in range(1, 5):
        name_col = f'Ataque{i} Nombre'
        type_col = f'Ataque{i} Tipo'
        power_col = f'Ataque{i} Poder'
        if name_col in df_attacks.columns and type_col in df_attacks.columns and power_col in df_attacks.columns:
            for _, row in df_attacks.iterrows():
                if pd.notna(row[name_col]) and pd.notna(row[type_col]) and pd.notna(row[power_col]):
                    attacks_dict[row[name_col]] = Attack(row[name_col], row[type_col], row[power_col])

    pokemons = []
    for _, row in df_pokemon.iterrows():
        pokemon_attacks = []
        for i in range(1, 5):
            name_col = f'Ataque{i} Nombre'
            if name_col in row and pd.notna(row[name_col]) and row[name_col] in attacks_dict:
                pokemon_attacks.append(attacks_dict[row[name_col]])
        selected_attacks = random.sample(pokemon_attacks, min(4, len(pokemon_attacks)))
        pokemons.append({
            'name': row['Nombre'],
            'type': row['Tipo(s)'],
            'hp': row['HP'],
            'max_hp': row['HP'],
            'attack': row['Ataque'],
            'defense': row['Defensa'],
            'speed': row['Velocidad'],
            'attacks': selected_attacks,
            'image_path': row['Ruta Imagen']
        })

    return pokemons

def main():
    all_pokemons = load_data_from_excel("Pokemons.xlsx")
    app = PokemonBattleGUI(all_pokemons)
    app.run()

if __name__ == "__main__":
    main()