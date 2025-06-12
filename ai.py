from trainer import Trainer
from battle import Battle
import random
import copy

class AI:
    def __init__(self, trainer):
        self.trainer = trainer
        self.max_depth = 3  # Profundidad máxima para el algoritmo minimax

    def evaluate_battle(self, battle):
        """Función de evaluación mejorada que considera múltiples factores."""
        score = 0
        current_trainer = battle.get_current_trainer()
        opponent_trainer = battle.get_opponent_trainer()
        
        # Evaluar Pokémon activo
        active_pokemon = current_trainer.active_pokemon
        opponent_pokemon = opponent_trainer.active_pokemon
        
        # Evaluar HP relativo
        active_hp_ratio = active_pokemon['hp'] / active_pokemon['max_hp']
        opponent_hp_ratio = opponent_pokemon['hp'] / opponent_pokemon['max_hp']
        score += (active_hp_ratio - opponent_hp_ratio) * 100
        
        # Evaluar ventaja de tipo
        for attack in active_pokemon['attacks']:
            if attack is None:
                continue
            type_effectiveness = battle.get_type_effectiveness(attack.type, opponent_pokemon['type'])
            score += type_effectiveness * 30
        
        # Evaluar estadísticas
        score += active_pokemon['attack'] * 0.5
        score += active_pokemon['defense'] * 0.3
        score += active_pokemon['speed'] * 0.4
        
        # Evaluar Pokémon disponibles
        available_pokemon = len([p for p in current_trainer.pokemon_list if p['hp'] > 0])
        opponent_available = len([p for p in opponent_trainer.pokemon_list if p['hp'] > 0])
        score += (available_pokemon - opponent_available) * 50
        
        # Penalización por Pokémon debilitado
        if active_pokemon['hp'] <= 0:
            score -= 100
            
        return score

    def minimax(self, battle, depth, alpha, beta, maximizing_player):
        """Implementación mejorada del algoritmo minimax con poda alfa-beta."""
        if depth == 0 or battle.battle_over():
            return self.evaluate_battle(battle)

        current_trainer = battle.get_current_trainer()
        attacks = current_trainer.active_pokemon['attacks']

        if maximizing_player:
            max_eval = float('-inf')
            for attack in attacks:
                if attack is None:
                    continue
                cloned_battle = self.clone_battle(battle)
                attacker = cloned_battle.get_current_trainer().active_pokemon
                defender = cloned_battle.get_opponent_trainer().active_pokemon
                try:
                    damage = cloned_battle.perform_attack(attack, attacker, defender)
                    # Evaluar el resultado inmediato del ataque
                    if damage > 0:
                        max_eval = max(max_eval, damage * 0.5)
                except Exception:
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
            for attack in attacks:
                if attack is None:
                    continue
                cloned_battle = self.clone_battle(battle)
                attacker = cloned_battle.get_current_trainer().active_pokemon
                defender = cloned_battle.get_opponent_trainer().active_pokemon
                try:
                    damage = cloned_battle.perform_attack(attack, attacker, defender)
                    # Evaluar el resultado inmediato del ataque
                    if damage > 0:
                        min_eval = min(min_eval, -damage * 0.5)
                except Exception:
                    continue
                cloned_battle.switch_turn()
                eval = self.minimax(cloned_battle, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def choose_best_attack(self, battle):
        # Si no hay ataques disponibles, retornar -1
        if not self.trainer.active_pokemon['attacks']:
            return -1
            
        # Si solo hay un ataque, usarlo
        if len(self.trainer.active_pokemon['attacks']) == 1:
            return 0
            
        # Clonar la batalla para simular
        cloned_battle = self.clone_battle(battle)
        
        # Evaluar cada ataque posible
        best_score = float('-inf')
        best_index = 0
        
        for i, attack in enumerate(self.trainer.active_pokemon['attacks']):
            # Simular el ataque
            damage = cloned_battle.execute_attack(self.trainer, battle.trainer1, attack)
            
            # Calcular la puntuación basada en el daño causado
            score = damage
            
            # Actualizar el mejor ataque si es necesario
            if score > best_score:
                best_score = score
                best_index = i
        
        return best_index

    def clone_battle(self, battle):
        # Clonar los entrenadores y sus Pokémon
        t1_pokemons = [self.clone_pokemon(p) for p in battle.trainer1.pokemons]
        t2_pokemons = [self.clone_pokemon(p) for p in battle.trainer2.pokemons]
        
        # Crear nuevos entrenadores con los Pokémon clonados
        t1 = Trainer(battle.trainer1.name, t1_pokemons)
        t2 = Trainer(battle.trainer2.name, t2_pokemons)
        
        # Establecer los Pokémon activos
        t1.active_pokemon = t1_pokemons[battle.trainer1.pokemons.index(battle.trainer1.active_pokemon)]
        t2.active_pokemon = t2_pokemons[battle.trainer2.pokemons.index(battle.trainer2.active_pokemon)]
        
        # Crear una nueva batalla con los entrenadores clonados
        cloned_battle = Battle(t1, t2)
        return cloned_battle

    def clone_pokemon(self, pokemon):
        """Crea una copia profunda de un Pokémon."""
        return {
            'name': pokemon['name'],
            'type': pokemon['type'],
            'hp': pokemon['hp'],
            'max_hp': pokemon['max_hp'],
            'attack': pokemon['attack'],
            'defense': pokemon['defense'],
            'speed': pokemon['speed'],
            'attacks': pokemon['attacks'].copy(),
            'image_path': pokemon['image_path']
        }

def evaluate_state(battle, trainer):
    """Evalúa el estado actual de la batalla para un entrenador."""
    score = 0
    opponent = battle.trainer2 if trainer == battle.trainer1 else battle.trainer1
    
    # Evaluar Pokémon activo
    active_pokemon = trainer.active_pokemon
    opponent_pokemon = opponent.active_pokemon
    
    # Evaluar HP
    score += (active_pokemon['hp'] / active_pokemon['max_hp']) * 100
    score -= (opponent_pokemon['hp'] / opponent_pokemon['max_hp']) * 100
    
    # Evaluar ventaja de tipo
    if active_pokemon['type'] in battle.type_chart and opponent_pokemon['type'] in battle.type_chart[active_pokemon['type']]:
        type_advantage = battle.type_chart[active_pokemon['type']][opponent_pokemon['type']]
        score += type_advantage * 50
    
    # Evaluar estadísticas
    score += active_pokemon['attack'] * 0.5
    score += active_pokemon['defense'] * 0.3
    score += active_pokemon['speed'] * 0.4
    
    # Evaluar Pokémon en el equipo
    for pokemon in trainer.pokemon_list:
        if pokemon['hp'] > 0:
            score += 30  # Bonus por Pokémon disponible
    
    return score

def minimax(battle, depth, alpha, beta, is_maximizing):
    """Implementación mejorada del algoritmo minimax con poda alfa-beta."""
    if depth == 0 or battle.battle_over():
        return evaluate_state(battle, battle.trainer1 if is_maximizing else battle.trainer2)
    
    current_trainer = battle.trainer1 if is_maximizing else battle.trainer2
    opponent_trainer = battle.trainer2 if is_maximizing else battle.trainer1
    
    if is_maximizing:
        max_eval = float('-inf')
        # Evaluar todos los ataques posibles
        for attack in current_trainer.active_pokemon['attacks']:
            # Simular el ataque
            battle_copy = copy.deepcopy(battle)
            damage = battle_copy.perform_attack(attack, 
                                              battle_copy.trainer1.active_pokemon,
                                              battle_copy.trainer2.active_pokemon)
            
            # Evaluar el resultado
            eval = minimax(battle_copy, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        # Evaluar todos los ataques posibles del oponente
        for attack in opponent_trainer.active_pokemon['attacks']:
            # Simular el ataque
            battle_copy = copy.deepcopy(battle)
            damage = battle_copy.perform_attack(attack,
                                              battle_copy.trainer2.active_pokemon,
                                              battle_copy.trainer1.active_pokemon)
            
            # Evaluar el resultado
            eval = minimax(battle_copy, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(battle, depth=3):
    """Obtiene el mejor movimiento para la IA."""
    best_score = float('-inf')
    best_attack = None
    
    # Evaluar cada ataque posible
    for attack in battle.trainer1.active_pokemon['attacks']:
        # Simular el ataque
        battle_copy = copy.deepcopy(battle)
        damage = battle_copy.perform_attack(attack,
                                          battle_copy.trainer1.active_pokemon,
                                          battle_copy.trainer2.active_pokemon)
        
        # Evaluar el resultado
        score = minimax(battle_copy, depth - 1, float('-inf'), float('inf'), False)
        
        # Actualizar el mejor ataque si es necesario
        if score > best_score:
            best_score = score
            best_attack = attack
    
    return best_attack
