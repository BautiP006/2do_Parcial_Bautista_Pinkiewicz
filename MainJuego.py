import pygame
from BaseV2 import *
import csv
from Funciones import *
import random
# from Estadisticas import cargar_preguntas_con_estadisticas, actualizar_estadisticas, guardar_preguntas_con_estadisticas
# Preguntas = cargar_preguntas_con_estadisticas()

# --- Variables globales y configuración ---
racha_correctas = 0
comodines = {"bomba": True, "x2": True, "doble_chance": True, "pasar": True}
bomba_oculta = []
x2_activado = False
doble_chance_activado = False
ya_usó_doble_chance = False

# Carga imágenes de comodines
imagen_bomba = pygame.image.load("bomba.png")
imagen_x2 = pygame.image.load("x2.png")
imagen_doble = pygame.image.load("doble_chance.png")
imagen_pasar = pygame.image.load("pasar.png")
imagenes_comodines = {
    "bomba": imagen_bomba,
    "x2": imagen_x2,
    "doble_chance": imagen_doble,
    "pasar": imagen_pasar
}

# Definir tamaños
TAMAÑO_PREGUNTA = (800, 100)
TAMAÑO_RESPUESTA = (700, 60)

# Al inicio de MainJuego.py
pantalla = pygame.display.set_mode((1024, 768))  # O el tamaño que desees
imagen_fondo = pygame.image.load("ImagenRespu.png")
imagen_fondo = pygame.transform.scale(imagen_fondo, (pantalla.get_width(), pantalla.get_height()))

# --- Cargar preguntas ---
Preguntas = []
with open('Preguntas.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):
        try:
            Preguntas.append({
                "pregunta": row["pregunta"],
                "respuesta_1": row["respuesta_1"],
                "respuesta_2": row["respuesta_2"],
                "respuesta_3": row["respuesta_3"],
                "respuesta_4": row["respuesta_4"],
                "respuesta_correcta": int(row["respuesta_correcta"])  # Del 1 al 4
            })
        except Exception as e:
            print(f"❌ Error en la fila {i + 2}: {e}")
            print(f"Contenido problemático: {row}")
lista_preguntas = Preguntas.copy()

def mezclar_lista(lista):
    random.shuffle(lista)
    return lista

# Inicializar pygame y definir colores
pygame.init()
COLOR_AZUL = (0, 120, 255)
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)

# --- Crear superficies para pregunta y respuestas ---
cartas_respuestas = []
for i in range(4):
    cuadro_respuesta = {}
    cuadro_respuesta["superficie"] = pygame.Surface(TAMAÑO_RESPUESTA)
    cuadro_respuesta["rectangulo"] = cuadro_respuesta["superficie"].get_rect()
    cartas_respuestas.append(cuadro_respuesta)

fuente_pregunta = pygame.font.SysFont("Arial Narrow", 30)
fuente_respuesta = pygame.font.SysFont("Arial Narrow", 23)
fuente_texto = pygame.font.SysFont("Arial Narrow", 25)

mezclar_lista(lista_preguntas)
indice = 0
bandera_respuesta = False
bandera_mostrar = True

TIEMPO_PREGUNTA = 15  # segundos por pregunta
tiempo_restante = TIEMPO_PREGUNTA
ultimo_tick = pygame.time.get_ticks()

# Al inicio del archivo, agrega:
tiempo_feedback = 0

def mostrar_juego(pantalla, cola_eventos, datos_juego):
    global indice, bandera_respuesta, bandera_mostrar, tiempo_restante, ultimo_tick
    global racha_correctas, bomba_oculta, x2_activado, doble_chance_activado, ya_usó_doble_chance
    global tiempo_feedback, comodines

    retorno = "juego"
    ahora = pygame.time.get_ticks()

    # --- Fondo de pantalla ---
    pantalla.blit(imagen_fondo, (0, 0))

    # --- Actualizar tiempo por pregunta ---
    if tiempo_feedback == 0:
        if ahora - ultimo_tick >= 1500:  # Cada 1500 ms (1.5 segundos)
            tiempo_restante -= 1
            ultimo_tick = ahora
            if tiempo_restante <= 0:
                ERROR_SONIDO.play()
                datos_juego["vidas"] -= 1
                datos_juego["puntuacion"] -= 2
                if datos_juego["vidas"] < 0:
                    datos_juego["vidas"] = 0
                racha_correctas = 0
                bandera_respuesta = True
                bandera_mostrar = True
                tiempo_feedback = ahora  

    # --- Pregunta en recuadro azul centrado arriba ---
    TAM_CUADRO = (800, 100)
    POS_CUADRO = ((pantalla.get_width() - TAM_CUADRO[0]) // 2, 60)
    cuadro_pregunta = pygame.Surface(TAM_CUADRO)
    cuadro_pregunta.fill((0, 102, 204))  # Azul
    pregunta_actual = lista_preguntas[indice]
    texto_pregunta = fuente_pregunta.render(pregunta_actual["pregunta"], True, COLOR_BLANCO)
    rect_texto = texto_pregunta.get_rect(center=(TAM_CUADRO[0]//2, TAM_CUADRO[1]//2))
    cuadro_pregunta.blit(texto_pregunta, rect_texto)
    pantalla.blit(cuadro_pregunta, POS_CUADRO)

    # --- Respuestas en recuadros negros centrados debajo ---
    for i in range(4):
        x = (pantalla.get_width() - TAMAÑO_RESPUESTA[0]) // 2
        y = POS_CUADRO[1] + TAM_CUADRO[1] + 30 + i*70
        cuadro_respuesta = pygame.Surface(TAMAÑO_RESPUESTA)
        cuadro_respuesta.fill((0, 0, 0))  # Negro

        # Feedback visual: overlay verde o rojo si corresponde
        if tiempo_feedback > 0 and bandera_respuesta:
            pixel = cartas_respuestas[i]['superficie'].get_at((0,0))
            color_overlay = None
            if pixel[:3] == (0, 200, 0):
                color_overlay = (0, 200, 0, 120)
            elif pixel[:3] == (200, 0, 0):
                color_overlay = (200, 0, 0, 120)
            if color_overlay:
                overlay = pygame.Surface(TAMAÑO_RESPUESTA, pygame.SRCALPHA)
                overlay.fill(color_overlay)
                cuadro_respuesta.blit(overlay, (0, 0))

        # Texto de la respuesta
        if (i+1) in bomba_oculta:
            mostrar_texto(cuadro_respuesta, " ", (20, 20), fuente_respuesta, COLOR_BLANCO)
        else:
            mostrar_texto(cuadro_respuesta, pregunta_actual[f"respuesta_{i+1}"], (20, 20), fuente_respuesta, COLOR_BLANCO)

        cartas_respuestas[i]['superficie'] = cuadro_respuesta
        cartas_respuestas[i]['rectangulo'] = pantalla.blit(cuadro_respuesta, (x, y))

    # --- Comodines ---
    fuente_comodin = pygame.font.SysFont("Arial Narrow", 21)
    nombres_comodines = ["bomba", "x2", "doble_chance", "pasar"]
    botones_comodines = []
    for idx, nombre in enumerate(nombres_comodines):
        color = (0, 200, 0) if comodines[nombre] else (150, 150, 150)
        boton = pygame.Surface((120, 40))
        boton.fill(color)
        imagen = pygame.transform.scale(imagenes_comodines[nombre], (32, 32))
        boton.blit(imagen, (5, 4))
        mostrar_texto(boton, nombre.upper(), (45, 8), fuente_comodin, (255,255,255))
        x_boton = pantalla.get_width() - 150
        y_boton = pantalla.get_height() - 220 + idx*50
        rect = boton.get_rect(topleft=(x_boton, y_boton))
        pantalla.blit(boton, rect.topleft)
        botones_comodines.append((rect, nombre))

    # --- Info de juego ---
    mostrar_texto(pantalla, f"PUNTUACION: {datos_juego['puntuacion']}", (10, 10), fuente_texto, COLOR_NEGRO)
    mostrar_texto(pantalla, f"VIDAS: {datos_juego['vidas']}", (10, 40), fuente_texto, COLOR_NEGRO)
    mostrar_texto(pantalla, f"TIEMPO: {tiempo_restante}", (10, 70), fuente_texto, (200,0,0))

    # --- Feedback visual/sonoro antes de avanzar ---
    if tiempo_feedback > 0:
        pygame.display.flip()
        if ahora - tiempo_feedback > 700:  # 700 ms de feedback
            indice += 1
            if indice >= len(lista_preguntas):
                indice = 0
                mezclar_lista(lista_preguntas)
            bandera_respuesta = False
            bandera_mostrar = True
            tiempo_restante = TIEMPO_PREGUNTA
            bomba_oculta.clear()
            doble_chance_activado = False
            ya_usó_doble_chance = False
            tiempo_feedback = 0
            if datos_juego["vidas"] <= 0:
                return "terminado"
        else:
            return retorno

    # --- Procesar eventos SOLO si no se está mostrando feedback
    if tiempo_feedback == 0:
        for evento in cola_eventos:
            if evento.type == pygame.QUIT:
                retorno = "salir"
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # --- Comodines ---
                for rect, nombre in botones_comodines:
                    if rect.collidepoint(evento.pos) and comodines[nombre]:
                        comodines[nombre] = False
                        if nombre == "bomba":
                            bomba_oculta.clear()
                            correct = pregunta_actual["respuesta_correcta"]
                            opciones = [1,2,3,4]
                            opciones.remove(correct)
                            bomba_oculta = random.sample(opciones, 2)
                        elif nombre == "x2":
                            x2_activado = True
                        elif nombre == "doble_chance":
                            doble_chance_activado = True
                            ya_usó_doble_chance = False
                        elif nombre == "pasar":
                            indice += 1
                            if indice >= len(lista_preguntas):
                                indice = 0
                                mezclar_lista(lista_preguntas)
                            bandera_mostrar = True
                            tiempo_restante = TIEMPO_PREGUNTA
                            bomba_oculta.clear()
                        break
                # --- Respuestas ---
                for i in range(4):
                    if cartas_respuestas[i]['rectangulo'].collidepoint(evento.pos):
                        respuesta_usuario = i + 1
                        if verificar_respuesta(datos_juego, pregunta_actual, respuesta_usuario):
                            CLICK_SONIDO.play()
                            cartas_respuestas[i]['superficie'].fill((0, 200, 0))  # Verde
                            datos_juego["puntuacion"] += 5 if not x2_activado else 10
                            if x2_activado:
                                x2_activado = False
                            racha_correctas += 1
                            if racha_correctas == 5:
                                datos_juego["vidas"] += 1
                                racha_correctas = 0
                        else:
                            ERROR_SONIDO.play()
                            cartas_respuestas[i]['superficie'].fill((200, 0, 0))  # Rojo
                            datos_juego["vidas"] -= 1
                            if datos_juego["vidas"] < 0:
                                datos_juego["vidas"] = 0
                            datos_juego["puntuacion"] -= 2
                            racha_correctas = 0
                        bandera_respuesta = True
                        bandera_mostrar = True
                        tiempo_feedback = ahora  # Marca el inicio del feedback
                        break

    pygame.display.flip()
    return retorno


"""Cuando el usuario responde, pinta la opción de verde o rojo y suena el sonido.
Espera 700 ms mostrando el feedback antes de avanzar.
Descuenta vidas y suma/resta puntos correctamente.
El juego termina solo si las vidas llegan a 0.
¡Perfecto! Ya tienes el bloque de `mostrar_juego` bien armado y funcional en tu archivo.  
Solo asegúrate de que
- En MainJuego.py, el bloque que pegaste es correcto y cumple con todos los puntos de la consigna:
- Pregunta aleatoria.
- Cuatro opciones.
- Suma/resta puntos y vidas correctamente.
- Racha de 5 aciertos suma vida.
- Si se queda sin tiempo, pierde vida.
- Feedback visual y sonoro.
- Avanza solo después del feedback.
- Termina cuando se quedan sin vidas."""
