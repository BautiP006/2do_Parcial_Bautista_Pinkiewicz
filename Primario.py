import pygame
from BaseV2 import *
from MenuPrincipal import *
from MainJuego import *
from ConfiguracionV2 import *
from Tabla_Posiciones import *
from MenuFinal import *

ancho_ventana = 1152
alto_ventana = 864
VENTANA = (ancho_ventana, alto_ventana)

CANTIDAD_VIDAS = 3
FPS = 100  # Cuadros por segundo

comodines = {"bomba": True, "x2": True, "doble_chance": True, "pasar": True}

# Estado del juego
datos_juego = {
    "puntuacion": 0,
    "vidas": CANTIDAD_VIDAS,
    "nombre": "",
    "volumen_musica": 100,
    "racha": 0,
    "tiempo": 15,  # segundos por pregunta (puedes cambiarlo)
    "musica_activada": True
}

# Configuraciones Basicas
pygame.init()
pygame.mixer.init()
CLICK_SONIDO = pygame.mixer.Sound("click.mp3")
ERROR_SONIDO = pygame.mixer.Sound("error.mp3")
pygame.display.set_caption("Juego de Preguntas y Respuestas")
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)
pantalla = pygame.display.set_mode(VENTANA)
corriendo = True
reloj = pygame.time.Clock()
ventana_actual = "menu"
bandera_musica = False

# Inicialización de banderas para el juego
indice = 0
bandera_respuesta = False
bandera_mostrar = True
partida_iniciada = False

while corriendo:
    reloj.tick(FPS)
    cola_eventos = pygame.event.get()

    # Control de música
    pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
    if datos_juego["musica_activada"] and not bandera_musica:
        pygame.mixer.music.load("musica_inicio.mp3")
        pygame.mixer.music.play(-1)
        bandera_musica = True
    elif not datos_juego["musica_activada"] and bandera_musica:
        pygame.mixer.music.stop()
        bandera_musica = False

    if ventana_actual == "menu":
        partida_iniciada = False
        ventana_actual = mostrar_menu(pantalla, cola_eventos)

    elif ventana_actual == "juego":
        if not partida_iniciada:
            datos_juego["vidas"] = CANTIDAD_VIDAS
            datos_juego["puntuacion"] = 0
            datos_juego["nombre"] = ""
            datos_juego["racha"] = 0
            datos_juego["tiempo"] = 15
            indice = 0
            bandera_respuesta = False
            bandera_mostrar = True
            mezclar_lista(lista_preguntas)
            comodines = {"bomba": True, "x2": True, "doble_chance": True, "pasar": True}
            partida_iniciada = True
        ventana_actual = mostrar_juego(pantalla, cola_eventos, datos_juego)

    elif ventana_actual == "configuraciones":
        ventana_actual = mostrar_configuracion(pantalla, cola_eventos, datos_juego)

    elif ventana_actual == "rankings":
        ventana_actual = mostrar_rankings(pantalla, cola_eventos)

    elif ventana_actual == "terminado":
        partida_iniciada = False
        if bandera_musica:
            pygame.mixer.music.stop()
            bandera_musica = False
        ventana_actual = mostrar_fin_juego(pantalla, cola_eventos, datos_juego)

    elif ventana_actual == "salir":
        corriendo = False

    pygame.display.flip()

pygame.quit()