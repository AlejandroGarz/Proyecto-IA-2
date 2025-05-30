from pokemon import Pokemon

class Trainer:
    def __init__(self, name, pokemon_list):
        self.name = name
        self.pokemon_list = pokemon_list
        self.active_pokemon = pokemon_list[0] if pokemon_list else None

    def __str__(self):
        return f"{self.name} with active Pokemon: {self.active_pokemon}"

    def choose_attack(self, attack_index):
        if self.active_pokemon and 0 <= attack_index < len(self.active_pokemon.attacks):
            return self.active_pokemon.attacks[attack_index]
        return None

    def switch_pokemon(self, pokemon_index):
        if 0 <= pokemon_index < len(self.pokemon_list) and self.pokemon_list[pokemon_index].hp > 0:
            self.active_pokemon = self.pokemon_list[pokemon_index]
            return True
        return False

    def has_available_pokemon(self):
        return any(pokemon.hp > 0 for pokemon in self.pokemon_list)
