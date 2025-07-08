import pygame
import json
from datetime import datetime
# from Tabla_Posiciones import guardar_partida  # <-- ELIMINA o comenta esta línea
from Funciones import mostrar_texto

def mostrar_fin_juego(pantalla, cola_eventos, datos_juego):
    nombre = ""
    escribiendo = True
    fuente = pygame.font.SysFont("Arial Narrow", 30)
    while escribiendo:
        pantalla.fill((255,255,255))
        mostrar_texto(pantalla, "¡Juego terminado!", (100, 100), fuente, (0,0,0))
        mostrar_texto(pantalla, "Ingrese su nombre y presione ENTER:", (100, 200), fuente, (0,0,0))
        mostrar_texto(pantalla, nombre, (100, 250), fuente, (0,0,255))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre.strip() != "":
                    guardar_partida(nombre, datos_juego["puntuacion"])
                    return "menu"
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 15 and evento.unicode.isprintable():
                        nombre += evento.unicode
                        
def guardar_partida(nombre, puntaje):
    from datetime import datetime
    import json
    try:
        with open("partidas.json", "r", encoding="utf-8") as f:
            partidas = json.load(f)
    except:
        partidas = []
    partidas.append({
        "nombre": nombre,
        "puntaje": puntaje,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
    })
    partidas.sort(key=lambda x: x["puntaje"], reverse=True)
    with open("partidas.json", "w", encoding="utf-8") as f:
        json.dump(partidas, f, ensure_ascii=False, indent=2)

def mostrar_rankings(pantalla, cola_eventos):
    COLOR_FONDO = (230, 240, 255)
    COLOR_HEADER = (0, 120, 255)
    COLOR_TEXTO = (30, 30, 30)
    COLOR_LINEA = (180, 200, 230)
    fuente = pygame.font.SysFont("Arial Narrow", 30)
    fuente_header = pygame.font.SysFont("Arial Narrow", 32, bold=True)

    pantalla.fill(COLOR_FONDO)

    # Título
    mostrar_texto(pantalla, "TOP 10 PARTIDAS", (100, 30), fuente_header, COLOR_HEADER)

    # Encabezados de columnas
    mostrar_texto(pantalla, "Puesto", (100, 70), fuente, COLOR_HEADER)
    mostrar_texto(pantalla, "Nombre", (200, 70), fuente, COLOR_HEADER)
    mostrar_texto(pantalla, "Puntaje", (450, 70), fuente, COLOR_HEADER)
    mostrar_texto(pantalla, "Fecha", (600, 70), fuente, COLOR_HEADER)

    # Línea separadora
    pygame.draw.line(pantalla, COLOR_LINEA, (90, 105), (900, 105), 2)

    # Cargar partidas
    try:
        with open("partidas.json", "r", encoding="utf-8") as f:
            partidas = json.load(f)
    except:
        partidas = []
    partidas.sort(key=lambda x: x["puntaje"], reverse=True)

    # Mostrar filas del ranking
    for i, partida in enumerate(partidas[:10]):
        y = 110 + i*38
        color = (255,255,255) if i%2==0 else (220,230,250)
        pygame.draw.rect(pantalla, color, (90, y, 820, 36))
        mostrar_texto(pantalla, f"{i+1}", (110, y+5), fuente, COLOR_TEXTO)
        mostrar_texto(pantalla, partida['nombre'], (200, y+5), fuente, COLOR_TEXTO)
        mostrar_texto(pantalla, str(partida['puntaje']), (470, y+5), fuente, COLOR_TEXTO)
        mostrar_texto(pantalla, partida['fecha'], (600, y+5), fuente, COLOR_TEXTO)

    # Botón VOLVER
    boton_volver = pygame.Surface((140, 55))
    boton_volver.fill(COLOR_HEADER)
    mostrar_texto(boton_volver, "VOLVER", (25, 12), fuente, (255,255,255))
    rect_volver = boton_volver.get_rect(topleft=(30, 500))
    pantalla.blit(boton_volver, rect_volver.topleft)

    retorno = "rankings"
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if rect_volver.collidepoint(evento.pos):
                retorno = "menu"
    return retorno

