import pygame
from BaseV2 import *
from Funciones import mostrar_texto

# Definiciones necesarias
ancho_ventana = 1152
alto_ventana = 864
VENTANA = (ancho_ventana, alto_ventana)
TAMAÑO_BOTON = (250, 50)
COLOR_AZUL = (0, 120, 255)
COLOR_BLANCO = (255, 255, 255)

# Índices de los botones
BOTON_JUGAR = 0
BOTON_CONFIG = 1
BOTON_PUNTUACIONES = 2
BOTON_SALIR = 3

fuente_menu = pygame.font.SysFont("Arial Narrow", 30)
lista_botones = []

# Nombres de los botones
nombres_botones = ["JUGAR", "CONFIGURACION", "PUNTUACIONES", "SALIR"]

for i in range(4):
    boton = {}
    boton["superficie"] = pygame.Surface(TAMAÑO_BOTON)
    boton["superficie"].fill(COLOR_AZUL)
    mostrar_texto(boton["superficie"], nombres_botones[i], (25, 10), fuente_menu, COLOR_BLANCO)
    boton["rectangulo"] = boton["superficie"].get_rect()
    lista_botones.append(boton)

fondo = pygame.image.load("fondo.jpg")
fondo = pygame.transform.scale(fondo, VENTANA)

def mostrar_menu(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event]) -> str:
    """
    Muestra el menú principal y gestiona los eventos de los botones.
    Retorna un string indicando la siguiente pantalla a mostrar.
    """
    retorno = "menu"
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(lista_botones)):
                if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    if i == BOTON_SALIR:
                        retorno = "salir"
                    elif i == BOTON_JUGAR:
                        retorno = "juego"
                    elif i == BOTON_PUNTUACIONES:
                        retorno = "rankings"
                    elif i == BOTON_CONFIG:
                        retorno = "configuraciones"
        elif evento.type == pygame.QUIT:
            retorno = "salir"

    # Dibujar fondo
    pantalla.blit(fondo, (0, 0))

    # Dibujar botones
    lista_botones[BOTON_JUGAR]["rectangulo"] = pantalla.blit(lista_botones[BOTON_JUGAR]["superficie"], (125, 115))
    lista_botones[BOTON_CONFIG]["rectangulo"] = pantalla.blit(lista_botones[BOTON_CONFIG]["superficie"], (125, 195))
    lista_botones[BOTON_PUNTUACIONES]["rectangulo"] = pantalla.blit(lista_botones[BOTON_PUNTUACIONES]["superficie"], (125, 275))
    lista_botones[BOTON_SALIR]["rectangulo"] = pantalla.blit(lista_botones[BOTON_SALIR]["superficie"], (125, 355))

    return retorno