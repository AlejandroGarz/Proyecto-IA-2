from battle import Attack

class Trainer:
    def __init__(self, name, pokemons):
        self.name = name
        self.pokemons = pokemons
        self.active_pokemon = pokemons[0] if pokemons else None

    def __str__(self):
        return f"{self.name} with active Pokémon: {self.active_pokemon}"

    def choose_attack(self, attack_index):
        if self.active_pokemon and 0 <= attack_index < len(self.active_pokemon['attacks']):
            return self.active_pokemon['attacks'][attack_index]
        return None

    def switch_pokemon(self):
        # Buscar el siguiente Pokémon con HP > 0
        for pokemon in self.pokemons:
            if pokemon['hp'] > 0 and pokemon != self.active_pokemon:
                self.active_pokemon = pokemon
                return True
        return False  # No hay más Pokémon disponibles

    def has_available_pokemon(self):
        return any(pokemon['hp'] > 0 for pokemon in self.pokemons)
