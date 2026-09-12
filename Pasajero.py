import random
from enum import Enum, auto

class Estado(Enum):
    SENTADO = auto()
    SENTANDOME = auto()
    PARADO = auto()
    AVANZANDO = auto()
    LISTENING_AYO = auto()
    DOING_AYO = auto()
    ESPERANDO_VOLVLER_AYO = auto()

class Pasajero:
    def __init__(self, asiento, avion, P, T_SENTADO, T_CARRYON):
        self.carryOn = random.uniform(0, 1) <= P
        self.asiento = asiento
        self.pos = [0,2]

        self.ID_Carry = 1 if not self.carryOn else 4
        avion[0][2] = self.ID_Carry
        self.soyVentana = asiento[1] == 4 or asiento[1] == 0

        self.estado = Estado.PARADO

        self.HICE_AYO = False
        self.estoy_esperando = False
        self.tiempoAEsperar = 0

        self.T_ACOMODARME = T_SENTADO + self.carryOn * T_CARRYON
        self.T_PARARME = 3

        self.ID_AYO = 2 if asiento[1] < 2 else 3

    # Estoy a un asiento
    def estoyAUno(self):
        return self.pos[0] == self.asiento[0] - 1

    def llegueAFila(self):
        return self.pos[0] == self.asiento[0]

    def sentarme(self, avion):
        avion[self.asiento[0]][self.asiento[1]] = self.ID_Carry
        self.estado = Estado.SENTADO
        if self.HICE_AYO:
            avion[self.asiento[0]][2] = 8
        else:
            avion[self.asiento[0]][2] = 0

        self.pos = self.asiento.copy()

        if not self.soyVentana:
            if (self.asiento[1] == 1 and avion[self.asiento[0]][0] == 0) or (self.asiento[1] == 3 and avion[self.asiento[0]][4] == 0):
                self.estado = Estado.LISTENING_AYO
           
        return

    def avanzar(self, avion):
        avion[self.pos[0]][self.pos[1]] = 0
        self.pos[0]+=1
        avion[self.pos[0]][self.pos[1]] = self.ID_Carry

        self.estado = Estado.PARADO
        return

    def tengoAlguienEnFrente(self, avion):
        return avion[self.pos[0] + 1][2] != 0

    def asientoPasilloOcupado(self, avion):
        if self.asiento[1] == 4:
            return avion[self.asiento[0]][3]
        return avion[self.asiento[0]][1]

    def decidirObjetivo(self, avion):
        # Esperar
        self.tiempoAEsperar -= 1
        if self.tiempoAEsperar > 0: return

        match self.estado:
            case Estado.PARADO:
                self.analizarPARADO(avion)
            case Estado.AVANZANDO:
                self.analizarAVANZANDO(avion)
            case Estado.SENTANDOME:
                self.analizarSENTANDOME(avion)
            case Estado.LISTENING_AYO:
                self.analizarLISTENING_AYO(avion)
            case Estado.DOING_AYO:
                self.analizarDOING_AYO(avion)
            case Estado.ESPERANDO_VOLVLER_AYO:
                self.analizarESPERANDO_VOLVER_AYO(avion)
        return

    def analizarPARADO(self, avion):
        if self.tengoAlguienEnFrente(avion) and not self.llegueAFila(): return
        if not self.estoy_esperando:
            self.tiempoAEsperar = 3
            self.estoy_esperando = True
        else:
            self.estado = Estado.AVANZANDO
            self.estoy_esperando = False
        return

    def analizarAVANZANDO(self, avion):
        if self.soyVentana and self.estoyAUno() and self.asientoPasilloOcupado(avion) and not self.HICE_AYO:
            avion[self.asiento[0]][2] = self.ID_AYO
            self.estado = Estado.PARADO
            self.HICE_AYO = True
            return

        if self.llegueAFila():
            self.estado = Estado.SENTANDOME
            return

        if not self.estoy_esperando:
            if self.carryOn:
                self.tiempoAEsperar = 6
            else:
                self.tiempoAEsperar = 3
            self.estoy_esperando = True
            return

        self.estoy_esperando = False
        self.avanzar(avion)
        return

    def analizarSENTANDOME(self, avion):
        if not self.estoy_esperando:
            self.tiempoAEsperar = self.T_ACOMODARME
            self.estoy_esperando = True
            return

        self.estoy_esperando = False
        self.sentarme(avion)
        return

    def analizarLISTENING_AYO(self, avion):
        if avion[self.pos[0]][2] != self.ID_AYO: return

        if not self.estoy_esperando:
            self.tiempoAEsperar = self.T_PARARME
            self.estoy_esperando = True
            return

        self.estoy_esperando = False
        avion[self.pos[0]][self.pos[1]] = 0
        self.pos[1] = 2
        avion[self.pos[0]][self.pos[1]] = self.ID_Carry
        self.estado = Estado.DOING_AYO
        return

    def analizarDOING_AYO(self, avion):
        if self.tengoAlguienEnFrente(avion): return
        if not self.estoy_esperando:
            self.tiempoAEsperar = 3
            self.estoy_esperando = True
        else:
            self.estoy_esperando = False
            # MUEVO UNO ADELANTE
            avion[self.pos[0]][self.pos[1]] = 0
            self.pos[0]+=1
            avion[self.pos[0]][self.pos[1]] = self.ID_Carry
            self.estado = Estado.ESPERANDO_VOLVLER_AYO
        return

    def analizarESPERANDO_VOLVER_AYO(self, avion):
        if avion[self.pos[0]-1][2] != 8: return
        if not self.estoy_esperando:
            self.tiempoAEsperar = 6
            self.estoy_esperando = True
            return

        self.estoy_esperando = False
        avion[self.pos[0]][self.pos[1]] = 0
        self.sentarme(avion)
        return