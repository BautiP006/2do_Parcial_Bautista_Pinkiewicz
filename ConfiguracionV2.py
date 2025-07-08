import pygame
from BaseV2 import *
from Funciones import mostrar_texto

TAMAÑO_BOTON_VOLUMEN = (100,50)
TAMAÑO_BOTON_VOLVER = (120,50)
TAMAÑO_BOTON_MUSICA = (200,50)
COLOR_ROJO = (255,0,0)
COLOR_AZUL = (0,0,255)
COLOR_BLANCO = (255,255,255)
COLOR_NEGRO = (0,0,0)

pygame.init()

fuente_boton = pygame.font.SysFont("Arial Narrow",23)
fuente_volumen = pygame.font.SysFont("Arial Narrow",50)

boton_suma = {}
boton_suma["superficie"] = pygame.Surface(TAMAÑO_BOTON_VOLUMEN)
boton_suma["rectangulo"] = boton_suma["superficie"].get_rect()
boton_suma["superficie"].fill(COLOR_ROJO)

boton_resta = {}
boton_resta["superficie"] = pygame.Surface(TAMAÑO_BOTON_VOLUMEN)
boton_resta["rectangulo"] = boton_resta["superficie"].get_rect()
boton_resta["superficie"].fill(COLOR_ROJO)

boton_volver = {}
boton_volver["superficie"] = pygame.Surface(TAMAÑO_BOTON_VOLVER)
boton_volver["rectangulo"] = boton_volver["superficie"].get_rect()
boton_volver["superficie"].fill(COLOR_AZUL)

boton_musica = {}
boton_musica["superficie"] = pygame.Surface(TAMAÑO_BOTON_MUSICA)
boton_musica["rectangulo"] = boton_musica["superficie"].get_rect()
boton_musica["superficie"].fill(COLOR_AZUL)

def mostrar_configuracion(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    retorno = "configuraciones"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_suma["rectangulo"].collidepoint(evento.pos):
                if datos_juego["volumen_musica"] < 100:
                    datos_juego["volumen_musica"] += 5
                CLICK_SONIDO.play()
            elif boton_resta["rectangulo"].collidepoint(evento.pos):
                if datos_juego["volumen_musica"] > 0:
                    datos_juego["volumen_musica"] -= 5
                CLICK_SONIDO.play()
            elif boton_volver["rectangulo"].collidepoint(evento.pos):
                CLICK_SONIDO.play()
                retorno = "menu"
            elif boton_musica["rectangulo"].collidepoint(evento.pos):
                datos_juego["musica_activada"] = not datos_juego["musica_activada"]
                CLICK_SONIDO.play()

    pantalla.fill(COLOR_BLANCO)

    boton_suma["rectangulo"] = pantalla.blit(boton_suma['superficie'],(420,200))
    boton_resta["rectangulo"] = pantalla.blit(boton_resta['superficie'],(20,200))
    boton_volver["rectangulo"] = pantalla.blit(boton_volver['superficie'],(10,10))
    boton_musica["rectangulo"] = pantalla.blit(boton_musica['superficie'],(160,300))

    mostrar_texto(boton_suma["superficie"],"VOL +",(0,10),fuente_boton,COLOR_NEGRO)
    mostrar_texto(boton_resta["superficie"],"VOL -",(0,10),fuente_boton,COLOR_NEGRO)
    mostrar_texto(boton_volver["superficie"],"VOLVER",(10,10),fuente_boton,COLOR_BLANCO)
    mostrar_texto(pantalla,f"{datos_juego['volumen_musica']} %",(200,200),fuente_volumen,COLOR_NEGRO)

    estado_musica = "ON" if datos_juego["musica_activada"] else "OFF"
    mostrar_texto(boton_musica["superficie"], f"MUSICA {estado_musica}", (10, 10), fuente_boton, COLOR_BLANCO)

    return retorno