import random
from pokemon import Pokemon
from trainer import Trainer

class Battle:
    def __init__(self, trainer1, trainer2):
        self.trainer1 = trainer1
        self.trainer2 = trainer2
        self.turn = 0  # 0 for trainer1, 1 for trainer2
        self.type_chart = {
            "Normal": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 1},
            "Fire": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Grass": 2},
            "Water": {"Normal": 1, "Fire": 2, "Water": 0.5, "Grass": 0.5},
            "Grass": {"Normal": 1, "Fire": 0.5, "Water": 2, "Grass": 0.5},
        }

    def calculate_damage(self, attack, attacker, defender):
        if attack is None or attacker is None or defender is None:
            return 0 

        if attack.type not in self.type_chart:
            return attack.power  

        if defender.type not in self.type_chart[attack.type]:
            return attack.power  

        type_effectiveness = self.type_chart[attack.type][defender.type]
        damage = attack.power * type_effectiveness
        return damage


    def perform_attack(self, attack, attacker, defender):
        damage = self.calculate_damage(attack, attacker, defender)
        defender.hp -= damage
        if defender.hp < 0:
            defender.hp = 0
        return damage

    def check_fainted(self, pokemon):
        return pokemon.hp <= 0

    def switch_turn(self):
        self.turn = 1 - self.turn

    def get_current_trainer(self):
        return self.trainer1 if self.turn == 0 else self.trainer2

    def get_opponent_trainer(self):
        return self.trainer2 if self.turn == 0 else self.trainer1

    def battle_over(self):
        return not self.trainer1.has_available_pokemon() or not self.trainer2.has_available_pokemon()

    def get_winner(self):
        if not self.trainer1.has_available_pokemon():
            return self.trainer2
        elif not self.trainer2.has_available_pokemon():
            return self.trainer1
        else:
            return None
