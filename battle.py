import random

class Attack:
    def __init__(self, name, type, power):
        self.name = name
        self.type = type
        self.power = power

    def __str__(self):
        return f"{self.name} ({self.type}) - {self.power} power"

class Battle:
    def __init__(self, player_pokemon, ai_pokemon):
        self.player_pokemon = player_pokemon
        self.ai_pokemon = ai_pokemon
        self.current_turn = 1  # 1 para player_pokemon, 2 para ai_pokemon
        self.type_chart = {
            "Normal": {
                "Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1,
                "Ice": 1, "Fighting": 1, "Poison": 1, "Ground": 1, "Flying": 1,
                "Psychic": 1, "Bug": 1, "Rock": 0.5, "Ghost": 0, "Dragon": 1,
                "Dark": 1, "Steel": 0.5, "Fairy": 1
            },
            "Fire": {
                "Normal": 1, "Fire": 0.5, "Water": 0.5, "Grass": 2, "Electric": 1,
                "Ice": 2, "Fighting": 1, "Poison": 1, "Ground": 1, "Flying": 1,
                "Psychic": 1, "Bug": 2, "Rock": 0.5, "Ghost": 1, "Dragon": 0.5,
                "Dark": 1, "Steel": 2, "Fairy": 1
            },
            "Water": {
                "Normal": 1, "Fire": 2, "Water": 0.5, "Grass": 0.5, "Electric": 1,
                "Ice": 1, "Fighting": 1, "Poison": 1, "Ground": 2, "Flying": 1,
                "Psychic": 1, "Bug": 1, "Rock": 2, "Ghost": 1, "Dragon": 0.5,
                "Dark": 1, "Steel": 1, "Fairy": 1
            },
            "Grass": {
                "Normal": 1, "Fire": 0.5, "Water": 2, "Grass": 0.5, "Electric": 1,
                "Ice": 1, "Fighting": 1, "Poison": 0.5, "Ground": 2, "Flying": 0.5,
                "Psychic": 1, "Bug": 0.5, "Rock": 2, "Ghost": 1, "Dragon": 0.5,
                "Dark": 1, "Steel": 0.5, "Fairy": 1
            },
            "Electric": {
                "Normal": 1, "Fire": 1, "Water": 2, "Grass": 0.5, "Electric": 0.5,
                "Ice": 1, "Fighting": 1, "Poison": 1, "Ground": 0, "Flying": 2,
                "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 0.5,
                "Dark": 1, "Steel": 1, "Fairy": 1
            },
            "Ice": {
                "Normal": 1, "Fire": 0.5, "Water": 0.5, "Grass": 2, "Electric": 1,
                "Ice": 0.5, "Fighting": 1, "Poison": 1, "Ground": 2, "Flying": 2,
                "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 2,
                "Dark": 1, "Steel": 0.5, "Fairy": 1
            },
            "Fighting": {
                "Normal": 2, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1,
                "Ice": 2, "Fighting": 1, "Poison": 0.5, "Ground": 1, "Flying": 0.5,
                "Psychic": 0.5, "Bug": 0.5, "Rock": 2, "Ghost": 0, "Dragon": 1,
                "Dark": 2, "Steel": 2, "Fairy": 0.5
            },
            "Poison": {
                "Normal": 1, "Fire": 1, "Water": 1, "Grass": 2, "Electric": 1,
                "Ice": 1, "Fighting": 1, "Poison": 0.5, "Ground": 0.5, "Flying": 1,
                "Psychic": 1, "Bug": 1, "Rock": 0.5, "Ghost": 0.5, "Dragon": 1,
                "Dark": 1, "Steel": 0, "Fairy": 2
            },
            "Ground": {
                "Normal": 1, "Fire": 2, "Water": 1, "Grass": 0.5, "Electric": 2,
                "Ice": 1, "Fighting": 1, "Poison": 2, "Ground": 1, "Flying": 0,
                "Psychic": 1, "Bug": 0.5, "Rock": 2, "Ghost": 1, "Dragon": 1,
                "Dark": 1, "Steel": 2, "Fairy": 1
            },
            "Flying": {
                "Normal": 1, "Fire": 1, "Water": 1, "Grass": 2, "Electric": 0.5,
                "Ice": 1, "Fighting": 2, "Poison": 1, "Ground": 1, "Flying": 1,
                "Psychic": 1, "Bug": 2, "Rock": 0.5, "Ghost": 1, "Dragon": 1,
                "Dark": 1, "Steel": 0.5, "Fairy": 1
            },
            "Psychic": {
                "Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1,
                "Ice": 1, "Fighting": 2, "Poison": 2, "Ground": 1, "Flying": 1,
                "Psychic": 0.5, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 1,
                "Dark": 0, "Steel": 0.5, "Fairy": 1
            },
            "Bug": {
                "Normal": 1, "Fire": 0.5, "Water": 1, "Grass": 2, "Electric": 1,
                "Ice": 1, "Fighting": 0.5, "Poison": 0.5, "Ground": 1, "Flying": 0.5,
                "Psychic": 2, "Bug": 1, "Rock": 1, "Ghost": 0.5, "Dragon": 1,
                "Dark": 2, "Steel": 0.5, "Fairy": 0.5
            },
            "Rock": {
                "Normal": 1, "Fire": 2, "Water": 1, "Grass": 1, "Electric": 1,
                "Ice": 2, "Fighting": 0.5, "Poison": 1, "Ground": 0.5, "Flying": 2,
                "Psychic": 1, "Bug": 2, "Rock": 1, "Ghost": 1, "Dragon": 1,
                "Dark": 1, "Steel": 0.5, "Fairy": 1
            },
            "Ghost": {
                "Normal": 0, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1,
                "Ice": 1, "Fighting": 0, "Poison": 1, "Ground": 1, "Flying": 1,
                "Psychic": 2, "Bug": 1, "Rock": 1, "Ghost": 2, "Dragon": 1,
                "Dark": 0.5, "Steel": 1, "Fairy": 1
            },
            "Dragon": {
                "Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1,
                "Ice": 1, "Fighting": 1, "Poison": 1, "Ground": 1, "Flying": 1,
                "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 2,
                "Dark": 1, "Steel": 0.5, "Fairy": 0
            },
            "Dark": {
                "Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1,
                "Ice": 1, "Fighting": 0.5, "Poison": 1, "Ground": 1, "Flying": 1,
                "Psychic": 2, "Bug": 1, "Rock": 1, "Ghost": 2, "Dragon": 1,
                "Dark": 0.5, "Steel": 1, "Fairy": 0.5
            },
            "Steel": {
                "Normal": 1, "Fire": 0.5, "Water": 0.5, "Grass": 1, "Electric": 0.5,
                "Ice": 2, "Fighting": 1, "Poison": 1, "Ground": 1, "Flying": 1,
                "Psychic": 1, "Bug": 1, "Rock": 2, "Ghost": 1, "Dragon": 1,
                "Dark": 1, "Steel": 0.5, "Fairy": 2
            },
            "Fairy": {
                "Normal": 1, "Fire": 0.5, "Water": 1, "Grass": 1, "Electric": 1,
                "Ice": 1, "Fighting": 2, "Poison": 0.5, "Ground": 1, "Flying": 1,
                "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 2,
                "Dark": 2, "Steel": 0.5, "Fairy": 1
            }
        }

    def calculate_damage(self, attack, attacker, defender):
        if attack is None or attacker is None or defender is None:
            return 0

        # Obtener el ataque base del Pokémon atacante
        attack_stat = attacker.get('attack', 0)
        
        # Calcular el daño base sumando el poder del ataque y la estadística de ataque
        base_damage = attack.power + attack_stat
        
        # Obtener la defensa del Pokémon defensor
        defense_stat = defender.get('defense', 0)
        
        # Calcular el daño final restando la defensa
        final_damage = base_damage - defense_stat
        
        # Asegurarnos de que el daño no sea negativo
        if final_damage < 0:
            final_damage = 0

        # Aplicar el modificador de tipo si existe
        if attack.type in self.type_chart and defender['type'] in self.type_chart[attack.type]:
            type_effectiveness = self.type_chart[attack.type][defender['type']]
            final_damage *= type_effectiveness

        return final_damage

    def determine_first_attacker(self, pokemon1, pokemon2):
        """Determina qué Pokémon ataca primero basado en su velocidad."""
        speed1 = pokemon1.get('speed', 0)
        speed2 = pokemon2.get('speed', 0)
        
        if speed1 > speed2:
            return pokemon1, pokemon2
        elif speed2 > speed1:
            return pokemon2, pokemon1
        else:
            # Si tienen la misma velocidad, se decide al azar
            if random.random() < 0.5:
                return pokemon1, pokemon2
            else:
                return pokemon2, pokemon1

    def perform_attack(self, attack, attacker, defender):
        # Determinar quién ataca primero basado en la velocidad
        first_attacker, second_attacker = self.determine_first_attacker(attacker, defender)
        
        # Realizar el primer ataque
        damage1 = self.calculate_damage(attack, first_attacker, second_attacker)
        second_attacker['hp'] -= damage1
        if second_attacker['hp'] < 0:
            second_attacker['hp'] = 0
            
        # Verificar si el segundo Pokémon se debilitó
        if self.check_fainted(second_attacker):
            self.handle_fainted_pokemon(second_attacker)
            return damage1, 0  # Retornamos el daño del primer ataque y 0 para el segundo
            
        # Si el segundo Pokémon sigue vivo, puede contraatacar
        if attack is not None:  # Asumiendo que el segundo Pokémon usa el mismo ataque
            damage2 = self.calculate_damage(attack, second_attacker, first_attacker)
            first_attacker['hp'] -= damage2
            if first_attacker['hp'] < 0:
                first_attacker['hp'] = 0
                
            # Verificar si el primer Pokémon se debilitó
            if self.check_fainted(first_attacker):
                self.handle_fainted_pokemon(first_attacker)
                
            return damage1, damage2
            
        return damage1, 0

    def handle_fainted_pokemon(self, fainted_pokemon):
        # Determinar qué entrenador perdió el Pokémon
        trainer = self.player_pokemon if fainted_pokemon in self.player_pokemon.pokemons else self.ai_pokemon
        
        # Si el Pokémon debilitado es el activo, intentar cambiar al siguiente
        if fainted_pokemon == trainer.active_pokemon:
            self.switch_to_next_available_pokemon(trainer)

    def switch_to_next_available_pokemon(self, trainer):
        # Buscar el siguiente Pokémon con HP > 0
        for pokemon in trainer.pokemons:
            if pokemon['hp'] > 0:
                trainer.active_pokemon = pokemon
                return True
        return False

    def check_fainted(self, pokemon):
        return pokemon['hp'] <= 0

    def get_type_effectiveness(self, attack_type, defender_type):
        """Obtiene la efectividad de un tipo contra otro."""
        if attack_type in self.type_chart and defender_type in self.type_chart[attack_type]:
            return self.type_chart[attack_type][defender_type]
        return 1.0

    def get_available_pokemon(self, trainer):
        """Obtiene la lista de Pokémon disponibles (con HP > 0) de un entrenador."""
        return [pokemon for pokemon in trainer.pokemons if pokemon['hp'] > 0]

    def battle_over(self):
        return not self.player_pokemon.has_available_pokemon() or not self.ai_pokemon.has_available_pokemon()

    def get_winner(self):
        if not self.player_pokemon.has_available_pokemon():
            return self.ai_pokemon
        elif not self.ai_pokemon.has_available_pokemon():
            return self.player_pokemon
        else:
            return None

    def get_current_trainer(self):
        """Obtiene el entrenador actual basado en el turno."""
        return self.player_pokemon if self.current_turn == 1 else self.ai_pokemon

    def get_opponent_trainer(self):
        """Obtiene el entrenador oponente basado en el turno."""
        return self.ai_pokemon if self.current_turn == 1 else self.player_pokemon

    def execute_attack(self, attacker_trainer, defender_trainer, attack):
        attacker = attacker_trainer.active_pokemon
        defender = defender_trainer.active_pokemon
        
        # Calcular el daño base considerando ataque y defensa
        base_damage = attack.power * (attacker['attack'] / defender['defense'])
        
        # Aplicar multiplicador por tipo
        type_multiplier = self.get_type_multiplier(attack.type, defender['type'])
        
        # Calcular daño final
        final_damage = base_damage * type_multiplier
        
        # Aplicar el daño al defensor
        defender['hp'] = max(0, defender['hp'] - final_damage)
        
        return int(final_damage)  # Redondear el daño a un número entero

    def get_type_multiplier(self, attack_type, defender_type):
        # Tabla de efectividad de tipos
        type_chart = {
            "Normal": {
                "Normal": 1.0, "Fire": 1.0, "Water": 1.0, "Electric": 1.0,
                "Grass": 1.0, "Ice": 1.0, "Fighting": 1.0, "Poison": 1.0,
                "Ground": 1.0, "Flying": 1.0, "Psychic": 1.0, "Bug": 1.0,
                "Rock": 0.5, "Ghost": 0.0, "Dragon": 1.0, "Dark": 1.0,
                "Steel": 0.5, "Fairy": 1.0
            },
            "Fire": {
                "Normal": 1.0, "Fire": 0.5, "Water": 0.5, "Electric": 1.0,
                "Grass": 2.0, "Ice": 2.0, "Fighting": 1.0, "Poison": 1.0,
                "Ground": 1.0, "Flying": 1.0, "Psychic": 1.0, "Bug": 2.0,
                "Rock": 0.5, "Ghost": 1.0, "Dragon": 0.5, "Dark": 1.0,
                "Steel": 2.0, "Fairy": 1.0
            },
            "Water": {
                "Normal": 1.0, "Fire": 2.0, "Water": 0.5, "Electric": 1.0,
                "Grass": 0.5, "Ice": 1.0, "Fighting": 1.0, "Poison": 1.0,
                "Ground": 2.0, "Flying": 1.0, "Psychic": 1.0, "Bug": 1.0,
                "Rock": 2.0, "Ghost": 1.0, "Dragon": 0.5, "Dark": 1.0,
                "Steel": 1.0, "Fairy": 1.0
            },
            "Electric": {
                "Normal": 1.0, "Fire": 1.0, "Water": 2.0, "Electric": 0.5,
                "Grass": 0.5, "Ice": 1.0, "Fighting": 1.0, "Poison": 1.0,
                "Ground": 0.0, "Flying": 2.0, "Psychic": 1.0, "Bug": 1.0,
                "Rock": 1.0, "Ghost": 1.0, "Dragon": 0.5, "Dark": 1.0,
                "Steel": 1.0, "Fairy": 1.0
            },
            "Grass": {
                "Normal": 1.0, "Fire": 0.5, "Water": 2.0, "Electric": 1.0,
                "Grass": 0.5, "Ice": 1.0, "Fighting": 1.0, "Poison": 0.5,
                "Ground": 2.0, "Flying": 0.5, "Psychic": 1.0, "Bug": 0.5,
                "Rock": 2.0, "Ghost": 1.0, "Dragon": 0.5, "Dark": 1.0,
                "Steel": 0.5, "Fairy": 1.0
            }
        }
        
        # Obtener el multiplicador de la tabla
        if attack_type in type_chart and defender_type in type_chart[attack_type]:
            return type_chart[attack_type][defender_type]
        return 1.0  # Si no se encuentra en la tabla, daño normal

    def handle_player_turn(self, attack):
        # Ejecutar el ataque del jugador
        damage = self.execute_attack(self.player_pokemon, self.ai_pokemon, attack)
        
        # Verificar si el Pokémon de la IA ha sido derrotado
        if self.ai_pokemon.active_pokemon['hp'] <= 0:
            if not self.ai_pokemon.switch_pokemon():
                return "victory"  # Jugador gana
            return "ai_switched"  # IA cambió de Pokémon
        
        return "continue"  # La batalla continúa

    def handle_ai_turn(self, ai_attack):
        # Ejecutar el ataque de la IA
        damage = self.execute_attack(self.ai_pokemon, self.player_pokemon, ai_attack)
        
        # Verificar si el Pokémon del jugador ha sido derrotado
        if self.player_pokemon.active_pokemon['hp'] <= 0:
            if not self.player_pokemon.switch_pokemon():
                return "defeat"  # Jugador pierde
            return "player_switched"  # Jugador debe cambiar de Pokémon
        
        return "continue"  # La batalla continúa

    def get_battle_state(self):
        return {
            'player_pokemon': self.player_pokemon.active_pokemon,
            'ai_pokemon': self.ai_pokemon.active_pokemon,
            'player_available_pokemon': [p for p in self.player_pokemon.pokemons if p['hp'] > 0],
            'ai_available_pokemon': [p for p in self.ai_pokemon.pokemons if p['hp'] > 0]
        }

    def execute_turn(self, player_attack):
        result = {
            'player_attack': False,
            'ai_attack': False,
            'player_damage': 0,
            'ai_damage': 0,
            'ai_attack': None,
            'player_fainted': False,
            'ai_fainted': False
        }

        # Seleccionar ataque de la IA
        ai_attack = random.choice(self.ai_pokemon['attacks'])

        # Determinar quién ataca primero basado en la velocidad
        if self.player_pokemon['speed'] >= self.ai_pokemon['speed']:
            # Jugador ataca primero
            result['player_attack'] = True
            result['player_damage'] = player_attack.power
            self.ai_pokemon['hp'] -= player_attack.power

            # Verificar si el Pokémon de la IA ha muerto
            if self.ai_pokemon['hp'] <= 0:
                result['ai_fainted'] = True
                return result

            # IA ataca
            result['ai_attack'] = ai_attack
            result['ai_damage'] = ai_attack.power
            self.player_pokemon['hp'] -= ai_attack.power

            # Verificar si el Pokémon del jugador ha muerto
            if self.player_pokemon['hp'] <= 0:
                result['player_fainted'] = True
        else:
            # IA ataca primero
            result['ai_attack'] = ai_attack
            result['ai_damage'] = ai_attack.power
            self.player_pokemon['hp'] -= ai_attack.power

            # Verificar si el Pokémon del jugador ha muerto
            if self.player_pokemon['hp'] <= 0:
                result['player_fainted'] = True
                return result

            # Jugador ataca
            result['player_attack'] = True
            result['player_damage'] = player_attack.power
            self.ai_pokemon['hp'] -= player_attack.power

            # Verificar si el Pokémon de la IA ha muerto
            if self.ai_pokemon['hp'] <= 0:
                result['ai_fainted'] = True

        return result
