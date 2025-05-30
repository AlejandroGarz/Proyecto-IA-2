import copy

class Pokemon:
    def __init__(self, nombre, tipo, ps, ataques):
        self.nombre = nombre
        self.tipo = tipo
        self.ps = ps
        self.ataques = ataques

    def __repr__(self):
        return f"{self.nombre} ({self.tipo}) - PS: {self.ps}"


class Ataque:
    def __init__(self, nombre, poder, tipo):
        self.nombre = nombre
        self.poder = poder
        self.tipo = tipo

    def __repr__(self):
        return f"{self.nombre} ({self.tipo}) - Poder: {self.poder}"


class Entrenador:
    def __init__(self, nombre, pokemons, pokemon_activo=None):
        self.nombre = nombre
        self.pokemons = pokemons
        self.pokemon_activo = pokemon_activo

    def __repr__(self):
        return f"Entrenador: {self.nombre}, Pokemon Activo: {self.pokemon_activo.nombre if self.pokemon_activo else 'Ninguno'}"

def seleccionar_ataque(pokemon, nombre_ataque):
    """Selecciona un ataque del pokemon por su nombre."""
    for ataque in pokemon.ataques:
        if ataque.nombre == nombre_ataque:
            return ataque
    return None

def calcular_efectividad(tipo_ataque, tipo_defensor):
    """Calcula la efectividad de un ataque según los tipos."""
    # Subconjunto simplificado de tipos: fuego > planta, agua > fuego, planta > agua
    if tipo_ataque == "fuego" and tipo_defensor == "planta":
        return 2.0
    elif tipo_ataque == "agua" and tipo_defensor == "fuego":
        return 2.0
    elif tipo_ataque == "planta" and tipo_defensor == "agua":
        return 2.0
    elif tipo_ataque == tipo_defensor:
        return 0.5  # Ataques del mismo tipo son menos efectivos
    else:
        return 1.0

def calcular_danio(ataque, atacante, defensor):
    """Calcula el daño de un ataque."""
    efectividad = calcular_efectividad(ataque.tipo, defensor.tipo)
    danio = (ataque.poder * atacante.ps / 100) * efectividad
    return danio

def aplicar_danio(defensor, danio):
    """Aplica el daño a un pokemon."""
    defensor.ps -= danio
    if defensor.ps < 0:
        defensor.ps = 0

def esta_debilitado(pokemon):
    """Verifica si un pokemon está debilitado."""
    return pokemon.ps <= 0

def minimax(estado, profundidad, alfa, beta, es_maximizador):
    """Implementación de Minimax con poda alfa-beta."""
    # Implementar la lógica de Minimax aquí
    pass

def funcion_evaluacion(estado):
    """Función de evaluación para el estado del juego."""
    # Implementar la lógica de evaluación aquí
    pass

def deepcopy_estado(estado):
    """Crea una copia profunda del estado para la simulación."""
    return copy.deepcopy(estado)
