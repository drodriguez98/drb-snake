#       https://inventwithpython.com/wormy.py

import random, pygame, sys
from pygame.locals import *

#       CONSTANTES.

FPS = 15

ANCHO = 640
ALTO = 480
TAMAÑO_CELDA = 20

ANCHO_CELDA = int(ANCHO / TAMAÑO_CELDA)
ALTO_CELDA = int(ALTO / TAMAÑO_CELDA)

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
VERDE_OSCURO = (0, 155, 0)
GRIS_OSCURO  = (40, 40, 40)

COLOR_FONDO = NEGRO

ARRIBA = 'up'
ABAJO = 'down'
IZQUIERDA = 'left'
DERECHA = 'right'

CABEZA = 0 

#       El juego no se inicia si el ancho o el alto de la ventana no son múltiplos del tamaño de las celdas. 

assert ANCHO % TAMAÑO_CELDA == 0, "El ancho de la ventana debe ser un múltiplo del tamaño de la celda."
assert ALTO % TAMAÑO_CELDA == 0, "La altura de la ventana debe ser un múltiplo del tamaño de la celda."


#       FUNCIÓN PRINCIPAL.

def main():

    global RELOJ, VENTANA, FUENTE

    pygame.init()

    RELOJ = pygame.time.Clock()
    VENTANA = pygame.display.set_mode((ANCHO, ALTO))
    FUENTE = pygame.font.Font('freesansbold.ttf', 18)

    pygame.display.set_caption('Snake!')

    mostrar_pantalla_inicial()

    while True:

        inicio()
        game_over()

#       FUNCIÓN CON LA LÓGICA DEL JUEGO.

def inicio():

    #       Posiciones y dirección iniciales del gusano y la manzana.
    
    x = random.randint(5, ANCHO_CELDA - 6)
    y = random.randint(5, ALTO_CELDA - 6)

    coordenadas = [{'x': x, 'y': y},
                  {'x': x - 1, 'y': y},
                  {'x': x - 2, 'y': y}]

    direccion = DERECHA

    manzana = posicion_aleatoria()

    #      Bucle infinito que sale del juego si el usuario pulsa la tecla salir y cambia el valor de la dirección si se produce el evento asociado (pulsar alguna tecla de dirección). 
    
    while True:     

        for evento in pygame.event.get(): 

            if evento.type == QUIT:

                salir()

            if evento.type == KEYDOWN:

                if (evento.key == K_LEFT or evento.key == K_a) and direccion != DERECHA:

                    direccion = IZQUIERDA

                elif (evento.key == K_RIGHT or evento.key == K_d) and direccion != IZQUIERDA:

                    direccion = DERECHA

                elif (evento.key == K_UP or evento.key == K_w) and direccion != ABAJO:

                    direccion = ARRIBA

                elif (evento.key == K_DOWN or evento.key == K_s) and direccion != ARRIBA:

                    direccion = ABAJO

                elif evento.key == K_ESCAPE:

                    salir()

        #       Choques con los bordes: game over.

        if coordenadas[CABEZA]['x'] == -1 or coordenadas[CABEZA]['x'] == ANCHO_CELDA or coordenadas[CABEZA]['y'] == -1 or coordenadas[CABEZA]['y'] == ALTO_CELDA:

            return 

        #       Choques con la cola: game over.

        for cuerpo in coordenadas[1:]:

            if cuerpo['x'] == coordenadas[CABEZA]['x'] and cuerpo['y'] == coordenadas[CABEZA]['y']:

                return 
        
        #       Choque de la cabeza del gusano con la manzana: reubicación de la manzana. Si no, borramos el último segmento de la cola para dar efecto de movimiento.

        if coordenadas[CABEZA]['x'] == manzana['x'] and coordenadas[CABEZA]['y'] == manzana['y']:

            manzana = posicion_aleatoria() 

        else:

            del coordenadas[-1]     

        #       Nueva cabeza en función de la dirección del gusano, también para dar efecto de movimiento.

        if direccion == ARRIBA:

            nueva_cabeza = {'x': coordenadas[CABEZA]['x'], 'y': coordenadas[CABEZA]['y'] - 1}

        elif direccion == ABAJO:

            nueva_cabeza = {'x': coordenadas[CABEZA]['x'], 'y': coordenadas[CABEZA]['y'] + 1}

        elif direccion == IZQUIERDA:

            nueva_cabeza = {'x': coordenadas[CABEZA]['x'] - 1, 'y': coordenadas[CABEZA]['y']}

        elif direccion == DERECHA:

            nueva_cabeza = {'x': coordenadas[CABEZA]['x'] + 1, 'y': coordenadas[CABEZA]['y']}

        coordenadas.insert(0, nueva_cabeza)

        #       Elementos que se muestran en pantalla. Se actualiza continuamente según el valor de la constante FPS.

        VENTANA.fill(COLOR_FONDO)
        mostrar_cuadricula()
        mostrar_gusano(coordenadas)
        mostrar_manzana(manzana)
        mostrar_puntuacion(len(coordenadas) - 3)

        pygame.display.update()

        RELOJ.tick(FPS)

#       FUNCIÓN PARA EL TEXTO DE LA PANTALLA INICIAL Y GAME OVER.

def mostrar_pulsar_tecla():

    animacion_pulsar_tecla = FUENTE.render('Pulsa cualquier tecla para jugar', True, BLANCO)
    recta_pulsar_tecla = animacion_pulsar_tecla.get_rect()
    recta_pulsar_tecla.topleft = (ANCHO - 300, ALTO - 30)

    VENTANA.blit(animacion_pulsar_tecla, recta_pulsar_tecla)

#       FUNCIÓN QUE COMPRUEBA SI EL USUARIO PULSA ALGUNA TECLA PARA SALIR.

def teclas_salir():

    if len(pygame.event.get(QUIT)) > 0:

        salir()

    evento_salir = pygame.event.get(KEYUP)

    if len(evento_salir) == 0:

        return None

    if evento_salir[0].key == K_ESCAPE:

        salir()

    return evento_salir[0].key

#       FUNCIÓN QUE MUESTRA LA PANTALLA INICIAL Y LA ANIMACIÓN.

def mostrar_pantalla_inicial():

    fuente_animacion = pygame.font.Font('freesansbold.ttf', 100)
    texto_animacion_1 = fuente_animacion.render('Snake!', True, BLANCO, VERDE_OSCURO)
    texto_animacion_2 = fuente_animacion.render('Snake!', True, VERDE)

    grados_1 = 0
    grados_2 = 0

    #       Bucle infinito que rota las animaciones mientras el usuario no pulsa ninguna tecla.

    while True:

        VENTANA.fill(COLOR_FONDO)

        animacion_1 = pygame.transform.rotate(texto_animacion_1, grados_1)
        recta_animacion_1 = animacion_1.get_rect()
        recta_animacion_1.center = (ANCHO / 2, ALTO / 2)
        VENTANA.blit(animacion_1, recta_animacion_1)

        animacion_2 = pygame.transform.rotate(texto_animacion_2, grados_2)
        recta_animacion_2 = animacion_2.get_rect()
        recta_animacion_2.center = (ANCHO / 2, ALTO / 2)
        VENTANA.blit(animacion_2, recta_animacion_2)

        mostrar_pulsar_tecla()

        if teclas_salir():

            pygame.event.get() 
            return

        pygame.display.update()

        RELOJ.tick(FPS)

        grados_1 += 3   #   rota 3 grados por frame
        grados_2 += 7   #   rota 7 grados por frame

#       FUNCIÓN PARA SALIR DEL JUEGO.

def salir():

    pygame.quit()
    sys.exit()

#       FUNCIÓN PARA DAR POSICIONES ALEATORIAS A LA MANZANA.

def posicion_aleatoria():

    return {'x': random.randint(0, ANCHO_CELDA - 1), 'y': random.randint(0, ALTO_CELDA - 1)}


#       FUNCIÓN PARA MOSTRAR MENSAJE DE GAME OVER. 

def game_over():

    fuente_game_over = pygame.font.Font('freesansbold.ttf', 75)

    animacion_game = fuente_game_over.render('Game', True, BLANCO)
    animacion_over = fuente_game_over.render('Over', True, BLANCO)

    recta_game = animacion_game.get_rect()
    recta_over = animacion_over.get_rect()
    
    recta_game.midtop = (ANCHO / 2, 10 + 140)
    recta_over.midtop = (ANCHO / 2, recta_game.height + 75 + 100)

    VENTANA.blit(animacion_game, recta_game)
    VENTANA.blit(animacion_over, recta_over)

    mostrar_pulsar_tecla()

    pygame.display.update()
    pygame.time.wait(500)

    teclas_salir() 

    while True:

        if teclas_salir():
            pygame.event.get() 
            return

#       FUNCIÓN PARA MOSTRAR PUNTUACIÓN.

def mostrar_puntuacion(puntuacion):

    animacion_puntuacion = FUENTE.render('Puntuación: %s' % (puntuacion), True, BLANCO)
    recta_puntuacion = animacion_puntuacion.get_rect()
    recta_puntuacion.topleft = (ANCHO - 150, 10)

    VENTANA.blit(animacion_puntuacion, recta_puntuacion)

#       FUNCIÓN PARA MOSTRAR GUSANO.

def mostrar_gusano(coordenadas):

    for coord in coordenadas:

        x = coord['x'] * TAMAÑO_CELDA
        y = coord['y'] * TAMAÑO_CELDA

        recta_segmento = pygame.Rect(x, y, TAMAÑO_CELDA, TAMAÑO_CELDA)
        pygame.draw.rect(VENTANA, VERDE_OSCURO, recta_segmento)

        recta_segmento_interno = pygame.Rect(x + 4, y + 4, TAMAÑO_CELDA - 8, TAMAÑO_CELDA - 8)
        pygame.draw.rect(VENTANA, VERDE, recta_segmento_interno)

#       FUNCIÓN PARA MOSTRAR MANZANA.

def mostrar_manzana(coord):

    x = coord['x'] * TAMAÑO_CELDA
    y = coord['y'] * TAMAÑO_CELDA
    recta_manzana = pygame.Rect(x, y, TAMAÑO_CELDA, TAMAÑO_CELDA)

    pygame.draw.rect(VENTANA, ROJO, recta_manzana)

#       FUNCIÓN PARA MOSTRAR CUADRÍCULA.

def mostrar_cuadricula():

    #       Líneas verticales.

    for x in range(0, ANCHO, TAMAÑO_CELDA): 

        pygame.draw.line(VENTANA, GRIS_OSCURO, (x, 0), (x, ALTO))

    #       Líneas horizontales.

    for y in range(0, ALTO, TAMAÑO_CELDA): 

        pygame.draw.line(VENTANA, GRIS_OSCURO, (0, y), (ANCHO, y))


#       Comprueba si es el archivo principal.

if __name__ == '__main__':

    main()
