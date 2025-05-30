import random
from battle import Battle

class AI:
    def __init__(self, depth=2):
        self.depth = depth

    def minimax(self, battle, depth, alpha, beta, maximizing_player):
        if depth == 0 or battle.battle_over():
            return self.evaluate_battle(battle)

        if maximizing_player:
            max_eval = float('-inf')
            for attack_index in range(len(battle.get_current_trainer().active_pokemon.attacks)):
                attack = battle.get_current_trainer().choose_attack(attack_index)
                if attack:
                    # Simulate the attack
                    cloned_battle = self.clone_battle(battle)
                    attacker = cloned_battle.get_current_trainer().active_pokemon
                    defender = cloned_battle.get_opponent_trainer().active_pokemon
                    cloned_battle.perform_attack(attack, attacker, defender)
                    cloned_battle.switch_turn()

                    eval = self.minimax(cloned_battle, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for attack_index in range(len(battle.get_current_trainer().active_pokemon.attacks)):
                attack = battle.get_current_trainer().choose_attack(attack_index)
                if attack:
                    # Simulate the attack
                    cloned_battle = self.clone_battle(battle)
                    attacker = cloned_battle.get_current_trainer().active_pokemon
                    defender = cloned_battle.get_opponent_trainer().active_pokemon
                    cloned_battle.perform_attack(attack, attacker, defender)
                    cloned_battle.switch_turn()

                    eval = self.minimax(cloned_battle, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha cutoff
            return min_eval

    def choose_best_attack(self, battle):
        best_attack_index = -1
        best_eval = float('-inf')

        for attack_index in range(len(battle.get_current_trainer().active_pokemon.attacks)):
            attack = battle.get_current_trainer().choose_attack(attack_index)
            if attack:
                # Simulate the attack
                cloned_battle = self.clone_battle(battle)
                attacker = cloned_battle.get_current_trainer().active_pokemon
                defender = cloned_battle.get_opponent_trainer().active_pokemon
                cloned_battle.perform_attack(attack, attacker, defender)
                cloned_battle.switch_turn()

                eval = self.minimax(cloned_battle, self.depth, float('-inf'), float('inf'), False)

                if eval > best_eval:
                    best_eval = eval
                    best_attack_index = attack_index

        return best_attack_index

    def evaluate_battle(self, battle):
        # Evaluation function: HP difference + number of remaining Pokemon
        trainer1 = battle.trainer1
        trainer2 = battle.trainer2
        trainer1_hp = sum(pokemon.hp for pokemon in trainer1.pokemon_list)
        trainer2_hp = sum(pokemon.hp for pokemon in trainer2.pokemon_list)
        trainer1_pokemon_count = sum(1 for pokemon in trainer1.pokemon_list if pokemon.hp > 0)
        trainer2_pokemon_count = sum(1 for pokemon in trainer2.pokemon_list if pokemon.hp > 0)
        return (trainer2_hp - trainer1_hp) + (trainer2_pokemon_count - trainer1_pokemon_count) * 50

    def clone_battle(self, battle):
        # Create deep copies of trainers and their Pokemon
        trainer1_pokemon = [self.clone_pokemon(pokemon) for pokemon in battle.trainer1.pokemon_list]
        trainer2_pokemon = [self.clone_pokemon(pokemon) for pokemon in battle.trainer2.pokemon_list]

        cloned_trainer1 = type(battle.trainer1)(battle.trainer1.name, trainer1_pokemon)
        cloned_trainer2 = type(battle.trainer2)(battle.trainer2.name, trainer2_pokemon)

        cloned_battle = type(battle)(cloned_trainer1, cloned_trainer2)
        cloned_battle.turn = battle.turn

        # Set active Pokemon for cloned trainers
        cloned_trainer1.active_pokemon = cloned_trainer1.pokemon_list[battle.trainer1.pokemon_list.index(battle.trainer1.active_pokemon)] if battle.trainer1.active_pokemon else None
        cloned_trainer2.active_pokemon = cloned_trainer2.pokemon_list[battle.trainer2.pokemon_list.index(battle.trainer2.active_pokemon)] if battle.trainer2.active_pokemon else None

        return cloned_battle

    def clone_pokemon(self, pokemon):
        cloned_attacks = [type(attack)(attack.name, attack.type, attack.power) for attack in pokemon.attacks]
        cloned_pokemon = type(pokemon)(pokemon.name, pokemon.type, pokemon.hp, cloned_attacks)
        cloned_pokemon.max_hp = pokemon.max_hp  # Copy max_hp
        return cloned_pokemon
