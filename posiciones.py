import random

def posiciones_random(FILAS, ASIENTOS_VALIDOS, N_PASAJEROS, desde=0):
    return random.sample([(f, a) for f in range(desde+1, FILAS+1) for a in ASIENTOS_VALIDOS],N_PASAJEROS)

def posiciones_por_zona(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, K, reverse=True):
    posiciones = []
    asientos_por_fila = len(ASIENTOS_VALIDOS)
    filas_base = FILAS // K
    resto_filas = FILAS % K

    pasajeros_restantes = N_PASAJEROS
    desde = 0
    for i in range(K):
        filas_en_grupo = filas_base + (1 if i < resto_filas else 0)
        if filas_en_grupo == 0:
            continue

        hasta = desde + filas_en_grupo
        capacidad_grupo = filas_en_grupo * asientos_por_fila
        pasajeros_a_asignar = min(capacidad_grupo, pasajeros_restantes)

        if pasajeros_a_asignar > 0:
            temp = posiciones_random(hasta, ASIENTOS_VALIDOS, pasajeros_a_asignar, desde=desde)
            posiciones.extend(temp)
            pasajeros_restantes -= pasajeros_a_asignar

        desde = hasta

    if reverse:
        posiciones.reverse()
    return posiciones

def posiciones_por_WILMA_por_grupos(FILAS, N_PASAJEROS, K):
    posiciones = []
    filas_por_grupo = FILAS // K
    pasajeros_por_grupo = filas_por_grupo * 4
    resto = N_PASAJEROS - pasajeros_por_grupo * K

    for i in range(K):
        temp1 = posiciones_random(filas_por_grupo + filas_por_grupo*i, [0, 4], pasajeros_por_grupo//2, desde=filas_por_grupo*i)
        temp2 = posiciones_random(filas_por_grupo + filas_por_grupo*i, [1, 3], pasajeros_por_grupo - pasajeros_por_grupo//2, desde=filas_por_grupo*i)
        for pos in range(len(temp2)):
            posiciones.append(temp2[pos]) 
        for pos in range(len(temp1)):
            posiciones.append(temp1[pos]) 

    temp = posiciones_random(FILAS, [1,3], resto//2, desde=filas_por_grupo*K)
    if temp:
        for pos in range(len(temp)):
            posiciones.append(temp[pos])
    temp = posiciones_random(FILAS, [0,4], resto - resto//2, desde=filas_por_grupo*K)
    if temp:
        for pos in range(len(temp)):
            posiciones.append(temp[pos])

    posiciones.reverse()
    return posiciones

def posiciones_por_WILMA_random(FILAS, N_PASAJEROS):
    temp1 = posiciones_random(FILAS, [0, 4], N_PASAJEROS//2)
    temp2 = posiciones_random(FILAS, [1, 3], N_PASAJEROS - N_PASAJEROS//2)
    for pos in range(len(temp2)):
        temp1.append(temp2[pos])
    return temp1

def posiciones_por_WILMA_back_to_front(FILAS, N_PASAJEROS):
    temp1 = posiciones_por_zona(FILAS, N_PASAJEROS//2, [0, 4], FILAS)
    temp2 = posiciones_por_zona(FILAS, N_PASAJEROS - N_PASAJEROS//2, [1, 3], FILAS)
    for pos in range(len(temp2)):
        temp1.append(temp2[pos])
    return temp1

def posiciones_steffen(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS):
    orden_filas = (
        list(range(FILAS if FILAS % 2 == 0 else FILAS - 1, 0, -2))
        + list(range(FILAS if FILAS % 2 == 1 else FILAS - 1, 0, -2))
    )
    posiciones = [
        (f, a)
        for f in orden_filas
        for a in ASIENTOS_VALIDOS
    ]
    return posiciones[:N_PASAJEROS]

def posiciones_steffen2(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS):
    posiciones = []

    # Asientos ventana
    ventanas_der = ASIENTOS_VALIDOS[0]
    ventanas_izq = ASIENTOS_VALIDOS[3]

    # Asientos pasillo
    pasillo_der = ASIENTOS_VALIDOS[1]
    pasillo_izq = ASIENTOS_VALIDOS[2]

    grupos = [
        (ventanas_der, range(FILAS, 0, -2)),       # ventana der, filas impares
        (ventanas_izq, range(FILAS, 0, -2)),       # ventanas izq, filas impares
        (ventanas_der, range(FILAS - 1, 0, -2)),   # ventana der, filas pares
        (ventanas_izq, range(FILAS - 1, 0, -2)),   # ventanas izq, filas pares
        (pasillo_der, range(FILAS, 0, -2)),        # pasillos der, filas impares
        (pasillo_izq, range(FILAS, 0, -2)),        # pasillos izq, filas impares
        (pasillo_der, range(FILAS - 1, 0, -2)),    # pasillos der, filas pares
        (pasillo_izq, range(FILAS - 1, 0, -2))     # pasillos izq, filas pares
    ]

    for asiento, filas in grupos:
        for f in filas:
            posiciones.append((f, asiento))

    return posiciones[:N_PASAJEROS]