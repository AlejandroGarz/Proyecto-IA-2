import random
from battle import Battle

class AI:
    def __init__(self, depth=2):
        self.depth = depth

    def minimax(self, battle, depth, alpha, beta, maximizing_player):
        if depth == 0 or battle.battle_over():
            return self.evaluate_battle(battle)

        current_trainer = battle.get_current_trainer()
        attacks = current_trainer.active_pokemon.attacks

        if maximizing_player:
            max_eval = float('-inf')
            for attack_index, attack in enumerate(attacks):
                if attack is None:
                    continue
                cloned_battle = self.clone_battle(battle)
                attacker = cloned_battle.get_current_trainer().active_pokemon
                defender = cloned_battle.get_opponent_trainer().active_pokemon
                try:
                    cloned_battle.perform_attack(attack, attacker, defender)
                except (KeyError, AttributeError, TypeError):
                    continue
                cloned_battle.switch_turn()

                eval = self.minimax(cloned_battle, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for attack_index, attack in enumerate(attacks):
                if attack is None:
                    continue
                cloned_battle = self.clone_battle(battle)
                attacker = cloned_battle.get_current_trainer().active_pokemon
                defender = cloned_battle.get_opponent_trainer().active_pokemon
                try:
                    cloned_battle.perform_attack(attack, attacker, defender)
                except (KeyError, AttributeError, TypeError):
                    continue
                cloned_battle.switch_turn()

                eval = self.minimax(cloned_battle, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def choose_best_attack(self, battle):
        best_attack_index = -1
        best_eval = float('-inf')

        for attack_index, attack in enumerate(battle.get_current_trainer().active_pokemon.attacks):
            if attack is None:
                continue
            cloned_battle = self.clone_battle(battle)
            attacker = cloned_battle.get_current_trainer().active_pokemon
            defender = cloned_battle.get_opponent_trainer().active_pokemon
            try:
                cloned_battle.perform_attack(attack, attacker, defender)
            except (KeyError, AttributeError, TypeError):
                continue
            cloned_battle.switch_turn()

            eval = self.minimax(cloned_battle, self.depth, float('-inf'), float('inf'), False)
            if eval > best_eval:
                best_eval = eval
                best_attack_index = attack_index

        return best_attack_index

    def evaluate_battle(self, battle):
        trainer1 = battle.trainer1
        trainer2 = battle.trainer2

        trainer1_hp = sum(pokemon.hp for pokemon in trainer1.pokemon_list)
        trainer2_hp = sum(pokemon.hp for pokemon in trainer2.pokemon_list)

        trainer1_remaining = sum(1 for p in trainer1.pokemon_list if p.hp > 0)
        trainer2_remaining = sum(1 for p in trainer2.pokemon_list if p.hp > 0)

        return (trainer2_hp - trainer1_hp) + (trainer2_remaining - trainer1_remaining) * 50

    def clone_battle(self, battle):
        trainer1_pokemon = [self.clone_pokemon(p) for p in battle.trainer1.pokemon_list]
        trainer2_pokemon = [self.clone_pokemon(p) for p in battle.trainer2.pokemon_list]

        trainer1_class = type(battle.trainer1)
        trainer2_class = type(battle.trainer2)

        cloned_trainer1 = trainer1_class(battle.trainer1.name, trainer1_pokemon)
        cloned_trainer2 = trainer2_class(battle.trainer2.name, trainer2_pokemon)

        cloned_battle = Battle(cloned_trainer1, cloned_trainer2)
        cloned_battle.turn = battle.turn

        cloned_trainer1.active_pokemon = trainer1_pokemon[battle.trainer1.pokemon_list.index(battle.trainer1.active_pokemon)]
        cloned_trainer2.active_pokemon = trainer2_pokemon[battle.trainer2.pokemon_list.index(battle.trainer2.active_pokemon)]

        if hasattr(self, 'ensure_type_chart'):
            self.ensure_type_chart(cloned_battle.type_chart)

        return cloned_battle

    def clone_pokemon(self, pokemon):
        cloned_attacks = [type(a)(a.name, a.type, a.power) for a in pokemon.attacks if a is not None]
        clone = type(pokemon)(pokemon.name, pokemon.type, pokemon.hp, cloned_attacks)
        clone.max_hp = pokemon.max_hp
        return clone
