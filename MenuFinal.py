import pygame
import json
from datetime import datetime
from Funciones import mostrar_texto

# --- Inicializar pygame y constantes ---
pygame.init()

CUADRO_TEXTO = (400, 80)
COLOR_AZUL = (0, 120, 255)
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)

fuente = pygame.font.SysFont("Arial Narrow", 40)

cuadro = {}
cuadro["superficie"] = pygame.Surface(CUADRO_TEXTO)
cuadro["rectangulo"] = cuadro["superficie"].get_rect()
cuadro['superficie'].fill(COLOR_AZUL)

# --- Función para guardar la partida ---
def guardar_partida(nombre, puntaje):
    try:
        with open("partidas.json", "r", encoding="utf-8") as f:
            partidas = json.load(f)
    except FileNotFoundError:
        partidas = []

    partidas.append({
        "nombre": nombre,
        "puntaje": puntaje,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
    })

    partidas.sort(key=lambda x: x["puntaje"], reverse=True)

    with open("partidas.json", "w", encoding="utf-8") as f:
        json.dump(partidas, f, ensure_ascii=False, indent=2)

# --- Función para mostrar la pantalla final ---
def mostrar_fin_juego(pantalla, cola_eventos, datos_juego):
    nombre = ""
    escribiendo = True
    fuente = pygame.font.SysFont("Arial Narrow", 30)
    ranking_mostrado = False

    while escribiendo:
        pantalla.fill(COLOR_BLANCO)

        if not ranking_mostrado:
            mostrar_texto(pantalla, "¡Juego terminado!", (100, 100), fuente, COLOR_NEGRO)
            mostrar_texto(pantalla, "Ingrese su nombre y presione ENTER:", (100, 200), fuente, COLOR_NEGRO)
            mostrar_texto(pantalla, nombre, (100, 250), fuente, COLOR_AZUL)
        else:
            mostrar_texto(pantalla, "TOP 10 PARTIDAS", (100, 30), fuente, COLOR_NEGRO)
            try:
                with open("partidas.json", "r", encoding="utf-8") as f:
                    partidas = json.load(f)
            except:
                partidas = []
            partidas.sort(key=lambda x: x["puntaje"], reverse=True)
            for i, partida in enumerate(partidas[:10]):
                texto = f"{i+1}. {partida['nombre']} - {partida['puntaje']} pts - {partida['fecha']}"
                mostrar_texto(pantalla, texto, (100, 80 + i * 35), fuente, COLOR_NEGRO)

            # Botón VOLVER
            boton_volver = pygame.Surface((120, 50))
            boton_volver.fill(COLOR_AZUL)
            mostrar_texto(boton_volver, "VOLVER", (10, 10), fuente, COLOR_BLANCO)
            rect_volver = boton_volver.get_rect(topleft=(30, 500))
            pantalla.blit(boton_volver, rect_volver.topleft)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "menu"
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre.strip() != "":
                    guardar_partida(nombre, datos_juego["puntuacion"])
                    ranking_mostrado = True
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif len(nombre) < 15 and evento.unicode.isprintable():
                    nombre += evento.unicode
            elif evento.type == pygame.MOUSEBUTTONDOWN and ranking_mostrado:
                if rect_volver.collidepoint(evento.pos):
                    return "menu"
