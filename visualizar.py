import pygame
import sys

# --- Configuración ---
CELDA = 30          # se recalcula en iniciar_ventana() para que entre en pantalla
MARGEN = 2
COLUMNAS = 26
COL_PASILLO = 2  # columna que representa el pasillo, no un asiento

CELDA_MIN = 14
CELDA_MAX = 30
MARGEN_PANTALLA = 80  # px libres alrededor de la ventana (barra de tareas, etc.)

COLOR_FONDO = (24, 24, 26)        # piso / cabina
COLOR_PASILLO = (15, 15, 17)      # levemente más oscuro que el fondo
COLOR_ASIENTO = (200, 200, 205)   # base del asiento vacío
COLOR_RESPALDO = (170, 170, 178)  # respaldo del asiento vacío
COLOR_PERSONA = (46, 139, 87)     # base del asiento ocupado
COLOR_PERSONA_RESPALDO = (34, 105, 66)
COLOR_CABEZA = (222, 184, 135)    # "cabeza" de la persona sentada
COLOR_PERSONA_PASILLO = (70, 130, 190)   # cuerpo de quien camina por el pasillo
COLOR_CABEZA_PASILLO = (222, 184, 135)   # cabeza de quien camina por el pasillo

COLOR_PERSONA_CARRYON = (178, 34, 34)    # remera roja de quien camina con carry-on
COLOR_CARRYON = (90, 60, 30)             # cuerpo de la maleta
COLOR_CARRYON_MANIJA = (40, 40, 40)      # manija de la maleta


def es_pasillo(col_idx):
    return col_idx == COL_PASILLO


def dibujar_asiento(pantalla, x, y, ocupado):
    """Dibuja un asiento visto desde arriba: respaldo + base, y si está
    ocupado, una cabeza en el centro."""
    color_base = COLOR_PERSONA if ocupado else COLOR_ASIENTO
    color_respaldo = COLOR_PERSONA_RESPALDO if ocupado else COLOR_RESPALDO

    # Base del asiento (ocupa toda la celda)
    pygame.draw.rect(pantalla, color_base, (x, y, CELDA, CELDA), border_radius=6)

    # Respaldo: una franja más angosta arriba, para que se lea como asiento
    respaldo_h = CELDA * 0.35
    pygame.draw.rect(
        pantalla, color_respaldo,
        (x + 3, y+15, CELDA - 6, respaldo_h),
        border_radius=4
    )

    if ocupado:
        radio = CELDA * 0.22
        centro = (x + CELDA / 2, y + CELDA * 0.6)
        pygame.draw.circle(pantalla, COLOR_CABEZA, centro, radio)


def dibujar_persona_pasillo(pantalla, x, y):
    """Dibuja a alguien caminando por el pasillo, visto desde arriba:
    un cuerpo (círculo grande) + una cabeza (círculo chico)."""
    radio_cuerpo = CELDA * 0.30
    centro_cuerpo = (x + CELDA / 2, y + CELDA / 2)
    pygame.draw.circle(pantalla, COLOR_PERSONA_PASILLO, centro_cuerpo, radio_cuerpo)

    radio_cabeza = CELDA * 0.16
    centro_cabeza = (x + CELDA / 2, y + CELDA * 0.35)
    pygame.draw.circle(pantalla, COLOR_CABEZA_PASILLO, centro_cabeza, radio_cabeza)


def dibujar_persona_pasillo_carryon(pantalla, x, y):
    """Dibuja a alguien caminando por el pasillo con carry-on: mismo cuerpo
    que dibujar_persona_pasillo pero con remera roja, más una mini valija
    al lado. Solo se usa mientras la persona está en el pasillo (valor 4);
    al sentarse pasa a ser un 1 normal y ya no se dibuja el carry-on."""
    # Cuerpo corrido levemente para dejarle lugar a la valija al costado
    centro_cuerpo = (x + CELDA * 0.42, y + CELDA / 2)
    radio_cuerpo = CELDA * 0.28
    pygame.draw.circle(pantalla, COLOR_PERSONA_CARRYON, centro_cuerpo, radio_cuerpo)

    radio_cabeza = CELDA * 0.15
    centro_cabeza = (x + CELDA * 0.42, y + CELDA * 0.35)
    pygame.draw.circle(pantalla, COLOR_CABEZA_PASILLO, centro_cabeza, radio_cabeza)

    # Mini carry-on: un rectángulo angosto con una manija arriba
    carryon_w = CELDA * 0.22
    carryon_h = CELDA * 0.34
    carryon_x = x + CELDA * 0.68
    carryon_y = y + CELDA * 0.5 - carryon_h / 2
    pygame.draw.rect(
        pantalla, COLOR_CARRYON,
        (carryon_x, carryon_y, carryon_w, carryon_h),
        border_radius=3
    )
    manija_w = carryon_w * 0.5
    manija_h = CELDA * 0.08
    manija_x = carryon_x + (carryon_w - manija_w) / 2
    manija_y = carryon_y - manija_h + 2
    pygame.draw.rect(
        pantalla, COLOR_CARRYON_MANIJA,
        (manija_x, manija_y, manija_w, manija_h),
        border_radius=2
    )


def calcular_celda(filas, columnas):
    """Elige el tamaño de celda más grande posible que haga entrar toda
    la ventana en la pantalla del usuario, con un mínimo y un máximo."""
    info = pygame.display.Info()
    ancho_disp = info.current_w - MARGEN_PANTALLA
    alto_disp = info.current_h - MARGEN_PANTALLA

    celda_por_ancho = ancho_disp / columnas - MARGEN
    celda_por_alto = alto_disp / filas - MARGEN

    celda = min(celda_por_ancho, celda_por_alto)
    return int(max(CELDA_MIN, min(CELDA_MAX, celda)))


def iniciar_ventana(filas, columnas):
    global CELDA
    pygame.init()
    CELDA = calcular_celda(filas, columnas)

    ancho = columnas * (CELDA + MARGEN) + MARGEN
    alto = filas * (CELDA + MARGEN) + MARGEN
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Simulación de embarque")
    return pantalla


def dibujar(pantalla, avion):
    pantalla.fill(COLOR_FONDO)
    for fila_idx, fila in enumerate(avion):
        for col_idx, valor in enumerate(fila):
            x = col_idx * (CELDA + MARGEN) + MARGEN
            y = fila_idx * (CELDA + MARGEN) + MARGEN

            if es_pasillo(col_idx):
                # piso del pasillo
                pygame.draw.rect(pantalla, COLOR_PASILLO, (x, y, CELDA, CELDA))
                # si hay alguien caminando ahí, lo dibujamos encima
                if valor == 1:
                    dibujar_persona_pasillo(pantalla, x, y)
                elif valor == 4:
                    dibujar_persona_pasillo_carryon(pantalla, x, y)
                continue

            if valor == -1:
                # celda que no es un asiento real (ej. primera fila = zona de
                # cabina/puerta): se pinta como piso vacío, nadie se sienta ahí
                pygame.draw.rect(pantalla, COLOR_PASILLO, (x, y, CELDA, CELDA))
                continue

            # En los asientos, un 4 se trata igual que un 1 (una vez sentado
            # ya no lleva el carry-on visible)
            ocupado = (valor == 1 or valor == 4)
            dibujar_asiento(pantalla, x, y, ocupado)

    pygame.display.flip()