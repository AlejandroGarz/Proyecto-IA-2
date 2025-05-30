class Pokemon:
    def __init__(self, name, type, hp, attacks):
        self.name = name
        self.type = type
        self.hp = hp
        self.max_hp = hp
        self.attacks = attacks

    def __str__(self):
        return f"{self.name} ({self.type}) - HP: {self.hp}/{self.max_hp}"

class Attack:
    def __init__(self, name, type, power):
        self.name = name
        self.type = type
        self.power = power

    def __str__(self):
        return f"{self.name} ({self.type}) - Power: {self.power}"
