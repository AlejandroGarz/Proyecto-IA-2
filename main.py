import combate
import interfaz

# Inicialización
# Crear ataques
ataque_fuego = combate.Ataque("Llamarada", 50, "fuego")
ataque_agua = combate.Ataque("Pistola de Agua", 40, "agua")
ataque_planta = combate.Ataque("Hoja Afilada", 45, "planta")

# Crear pokemons
pokemon_jugador = combate.Pokemon("Charmander", "fuego", 100, [ataque_fuego, ataque_agua])
pokemon_ia = combate.Pokemon("Bulbasaur", "planta", 100, [ataque_planta, ataque_fuego])

# Crear entrenadores
jugador = combate.Entrenador("Ash", [pokemon_jugador])
ia = combate.Entrenador("Equipo Rocket", [pokemon_ia])

# Asignar pokemon iniciales
jugador.pokemon_activo = pokemon_jugador
ia.pokemon_activo = pokemon_ia

# Bucle del juego
juego_terminado = False
turno = "jugador"  # El jugador empieza

def aplicar_ataque(atacante, defensor, nombre_ataque):
    """Aplica un ataque del atacante al defensor."""
    ataque = combate.seleccionar_ataque(atacante.pokemon_activo, nombre_ataque)
    if ataque:
        danio = combate.calcular_danio(ataque, atacante.pokemon_activo, defensor.pokemon_activo)
        combate.aplicar_danio(defensor.pokemon_activo, danio)
        interfaz.mostrar_resultado(ataque, danio, defensor.pokemon_activo.nombre)
    else:
        print("Ataque no encontrado.")

def verificar_si_hay_ganador():
    """Verifica si hay un ganador."""
    if combate.esta_debilitado(jugador.pokemon_activo):
        return "IA"
    elif combate.esta_debilitado(ia.pokemon_activo):
        return "Jugador"
    return None

def cambiar_turno():
    """Cambia el turno."""
    global turno
    if turno == "jugador":
        turno = "ia"
    else:
        turno = "jugador"

while not juego_terminado:
    interfaz.mostrar_info_combate(jugador, ia)
    if turno == "jugador":
        ataque = interfaz.leer_entrada_usuario()
        aplicar_ataque(jugador, ia, ataque)
    else:
        print("Turno de la IA...")
        # ataque = combate.elegir_mejor_ataque_minimax()  # Implementar Minimax
        ataque = "Llamarada" #temporal
        aplicar_ataque(ia, jugador, ataque)

    interfaz.mostrar_estado_actual(jugador, ia)
    ganador = verificar_si_hay_ganador()
    if ganador:
        juego_terminado = True
        interfaz.mostrar_mensaje_fin_combate(ganador)
    else:
        cambiar_turno()
