from pokemon import Pokemon, Attack
from trainer import Trainer
from battle import Battle
from ai import AI

def create_pokemon(name, type, hp, attacks):
    attack_list = [Attack(attack[0], attack[1], attack[2]) for attack in attacks]
    return Pokemon(name, type, hp, attack_list)

def main():
    # Create Pokemon
    charmander = create_pokemon("Charmander", "Fire", 45, [("Scratch", "Normal", 45), ("Ember", "Fire", 45)])
    squirtle = create_pokemon("Squirtle", "Water", 44, [("Tackle", "Normal", 40), ("Water Gun", "Water", 40)])
    bulbasaur = create_pokemon("Bulbasaur", "Grass", 45, [("Tackle", "Normal", 40), ("Vine Whip", "Grass", 45)])
    pikachu = create_pokemon("Pikachu", "Electric", 35, [("Quick Attack", "Normal", 40), ("Thunder Shock", "Electric", 40)])

    # Create Trainers
    trainer1 = Trainer("Ash", [charmander])
    trainer2 = Trainer("AI", [bulbasaur])

    # Create AI
    ai = AI(depth=1)

    # Create Battle
    battle = Battle(trainer1, trainer2)

    # Game loop
    while not battle.battle_over():
        current_trainer = battle.get_current_trainer()
        opponent_trainer = battle.get_opponent_trainer()

        print(f"\n--- Turn {battle.turn + 1} ---")
        print(f"{current_trainer.name}'s turn")
        print(f"{current_trainer.active_pokemon}")
        print(f"{opponent_trainer.active_pokemon}")

        if current_trainer.name == "Ash":  # Human player
            # Display available attacks
            for i, attack in enumerate(current_trainer.active_pokemon.attacks):
                print(f"{i + 1}. {attack}")

            # Get player's choice
            while True:
                try:
                    choice = int(input("Choose an attack: ")) - 1
                    if 0 <= choice < len(current_trainer.active_pokemon.attacks):
                        attack = current_trainer.choose_attack(choice)
                        break
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Invalid input.")
        else:  # AI player
            attack_index = ai.choose_best_attack(battle)
            attack = current_trainer.choose_attack(attack_index)
            print(f"AI chose attack: {attack}")

        # Perform attack
        damage = battle.perform_attack(attack, current_trainer.active_pokemon, opponent_trainer.active_pokemon)
        print(f"{current_trainer.active_pokemon.name} used {attack.name} and dealt {damage} damage.")
        print(f"{opponent_trainer.active_pokemon}")

        # Check if opponent fainted
        if battle.check_fainted(opponent_trainer.active_pokemon):
            print(f"{opponent_trainer.active_pokemon.name} fainted!")
            if not opponent_trainer.has_available_pokemon():
                break
            else:
                #Switch pokemon
                opponent_trainer.switch_pokemon(0)
                print(f"{opponent_trainer.name} sends out {opponent_trainer.active_pokemon}!")

        # Switch turn
        battle.switch_turn()

    # Determine winner
    winner = battle.get_winner()
    print(f"\n--- Battle Over ---")
    print(f"{winner.name} wins!")

if __name__ == "__main__":
    main()
