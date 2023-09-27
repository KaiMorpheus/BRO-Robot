#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from comunicador import *
import threading

ev3 = EV3Brick()
motorA = Motor(Port.A)
motorB = Motor(Port.B)
motorC = Motor(Port.C)
motorD = Motor(Port.D)
sensorCorDireita = ColorSensor(Port.S4)
sensorCorEsquerda = ColorSensor(Port.S3)
sensorCorParede = ColorSensor(Port.S1)
sensorUT = UltrasonicSensor(Port.S2)
velocidade = 30
ACELERACAO = 100
motorEsquerda = motorA
motorDireita = motorB
motorAbreGarra = motorC
motorSobeDesceGarra= motorD
drive = DriveBase(motorEsquerda,motorDireita,56,120)
drive.settings(200, 200, 200, 200)
trocaModo = False
memoriaMovimentoDeterminado = False
leiturasCorEsquerda = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
leiturasCorDireita = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
leiturasCorParede = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
leituraUT = 0
leituraGiroscopio = 0
corPar = 0
corEsq = 0
corDir = 0
luzEsq = 0
luzDir = 0
GP = 1.1
GI = 0.015
GD = 0.07
controle = 0
controlePar = 0
reflexoDaLuzNaParede = 0
erroPar = 0
GANHOPROPORCIONALPAREDE = 1.2
velocidadePar = 60
erroAcumulado = 0
erroAnterior = 0
memoriaTaNaParede = False
isServidor = True
memoriaTerminouVolta = False
memoriaNaoLeMais = False
contador = 0
cravarParede = 0
com = Comunicador(ev3, True)
com.start()

class LerTudo(threading.Thread):
    def __init__(self):
        super().__init__
        threading.Thread.daemon = True

    def run(self):
        global leiturasCorDireita
        global leiturasCorEsquerda
        global corEsq
        global corDir
        global luzEsq
        global luzDir

        while True:

            luzEsq = sensorCorEsquerda.reflection()
            luzDir = sensorCorDireita.reflection()
            corEsq = sensorCorEsquerda.color()
            corDir = sensorCorDireita.color()

            leiturasCorDireita.append(corDir)
            leiturasCorDireita.pop(0)
            leiturasCorEsquerda.append(corEsq)
            leiturasCorEsquerda.pop(0)
            
            #wait(10)

#LerTudo().start()

def verificaVerdeEsquerda(): #Primeira Parte 
    for x in [14,13]:
        if (leiturasCorEsquerda[x] != Color.GREEN) :
            return False
    return True

def verificaVerdeDireita(): #Primeira Parte 
    for x in [14,13]:
        if (leiturasCorDireita[x] != Color.GREEN):
            return False
    return True

def verificaVerde180(): #Primeira Parte 
    for x in [14]:
        if (leiturasCorDireita[x] != Color.GREEN):
            return False
        if (leiturasCorEsquerda[x] != Color.GREEN):
            return False
    return True

def verificaPreto(): #Primeira Parte 

    dire = [leiturasCorDireita[14]]
    esq = [leiturasCorEsquerda[14]]
    pretos = [Color.BLACK]
    if(esq == pretos and dire == pretos) :
        return True
    return False
 
def verificaPretoDesvios(): #Primeira Parte
    
    if (verificaPreto()) :
        ev3.speaker.beep()
        ev3.speaker.beep()
        ev3.speaker.beep()

        global memoriaMovimentoDeterminado

        esq = [leiturasCorEsquerda[13]]
        dire = [leiturasCorDireita[13]]
        pretos = [Color.BLACK]
       
        if(esq == pretos and dire != pretos):
            memoriaMovimentoDeterminado = True
            drive.straight(30)
            drive.turn(40)
            #vira um pouco para direita e segue
            memoriaMovimentoDeterminado = False
            return
        elif (dire == pretos and esq != pretos):
            memoriaMovimentoDeterminado = True
            drive.straight(30)
            drive.turn(-40)
            # vira um pouco para esquerda e segue
            memoriaMovimentoDeterminado = False
            return
        memoriaMovimentoDeterminado = True
        drive.straight(40)
        #pulo de 4 cm
        memoriaMovimentoDeterminado = False
        return
            
def sequenciaMovimentosDesvioObjeto(): #Primeira Parte 
        memoriaMovimentoDeterminado = True
        wait(10)
        drive.turn(-70)
        drive.straight(160)
        drive.turn(70)
        drive.straight(380)
        drive.turn(70)
        drive.straight(150)
        drive.turn(-70)
        memoriaMovimentoDeterminado = False

def trancaParedeVerde(): #Segunda Parte 
    
    for x in [14]:
        if (leiturasCorParede[x] != Color.GREEN):
            return False
    return True

def trancaParede():
    for x in [14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]:
        if (leiturasCorParede[x] != Color.WHITE):
            return False
    return True

def sequenciaMovimentosDesvioParede():
    drive.straight(-25)
    drive.turn(95)

while com.ultimaMensagem() != "comece":
    pass

while True: #Primeira Parte

    corDir = sensorCorDireita.color()
    corEsq = sensorCorEsquerda.color()

    leiturasCorEsquerda.append(corEsq)
    leiturasCorDireita.append(corDir)
    leiturasCorEsquerda.pop(0)
    leiturasCorDireita.pop(0)

    verificaPretoDesvios()
    
    print(leiturasCorDireita)
    print(leiturasCorEsquerda)

    if (memoriaMovimentoDeterminado == True):
        leiturasCorEsquerda = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        leiturasCorDireita = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


    if (verificaVerde180()):
        memoriaMovimentoDeterminado = True
        drive.straight(5)
        drive.turn(180)
        memoriaMovimentoDeterminado = False
    elif (verificaVerdeDireita()):
        ev3.speaker.beep()  
        
        memoriaMovimentoDeterminado = True
        drive.straight(65)
        drive.turn(55)
        memoriaMovimentoDeterminado = False

    elif (verificaVerdeEsquerda()):
        ev3.speaker.beep()
        ev3.speaker.beep()

        memoriaMovimentoDeterminado = True
        drive.straight(65)
        drive.turn(-55)
        memoriaMovimentoDeterminado = False

    else:
        luzEsq = sensorCorEsquerda.reflection()
        luzDir = sensorCorDireita.reflection()
        erroAtual = luzEsq - luzDir
        controle = erroAtual * GP
        drive.drive(velocidade, controle)

    if (com.ultimaMensagem() == "rampa"):
        velocidade = 150
    else:
        velocidade = 35
    
    if (com.ultimaMensagem() == "terminouRampa"):
        break
    
    wait(10)
    
while True: #Segunda Parte

    drive.straight(450)
    drive.turn(60)
    velocidade = 35
    #motorSobeDesceGarra.run_angle(170, -200, then=Stop.HOLD, wait=False)
    com.enviarMensagem("abreGarra")

    motorAbreGarra.run_angle(100, -90, then=Stop.HOLD, wait=True)

    drive.turn(-40)
    break


com.enviarMensagem("resetaAngulo")
drive.stop()
drive.settings(35,35,35,35)

while True: #Segunda Parte
    print(leituraUT)
    leituraUT = sensorUT.distance(silent=False)

    if (leituraUT <= 200 and memoriaNaoLeMais == False):
        sequenciaMovimentosDesvioParede()

    corPar = sensorCorParede.color()
    leiturasCorParede.append(corPar)
    leiturasCorParede.pop(0)

    if (corPar != None):
        if contador < 0 :
            contador = 0
        contador += 1
        if (contador > 10):
            contador = 10
        drive.drive(velocidade, 4 * contador)

    else :
        if contador > 0 :
            contador = 0
        contador -= 1
        if (contador < -10):
            contador = -10
        drive.drive(velocidade, 4  * contador)

    if (com.ultimaMensagem() == "terminouVolta" and memoriaTerminouVolta == False):
        memoriaNaoLeMais = True
        drive.turn(30)
        drive.stop()
        #Termina de Abrir a Garra
        #Se aproxima da Parede
        drive.drive(35, 0)
        while (leituraUT > 220):
            leituraUT = sensorUT.distance(silent=False)

        drive.stop()
        com.enviarMensagem("terminaAbreGarra")
        motorAbreGarra.run_angle(40, -60, then=Stop.HOLD, wait=True)

        #Fecha as Garras
        drive.stop()
        com.enviarMensagem("FechaGarra")
        motorAbreGarra.run_angle(40, 160, then=Stop.HOLD, wait = True)

        drive.straight(-100)

        cravarParede = leituraUT
        drive.stop()
        drive.settings(30, 30, 30, 30)
        motorSobeDesceGarra.run_angle(170, -220, then=Stop.HOLD, wait=True)

        drive.straight(leituraUT)

        drive.stop()
        #motorSobeDesceGarra.run_angle(20, 200, then=Stop.HOLD, wait=False)
        drive.straight(-100)
        drive.stop()
        drive.turn(90)
        drive.stop()
        drive.settings(100, 100, 100, 100)
        motorAbreGarra.run_angle(100, -200, then=Stop.HOLD, wait=True)
        memoriaTerminouVolta = True
        memoriaNaoLeMais = False

    if (memoriaTerminouVolta == True):
        if (trancaParedeVerde()):

            drive.straight(-30)
            motorAbreGarra.run_angle(100, 105, then=Stop.HOLD, wait=True)
            drive.turn(150)
            drive.stop()
            drive.settings(30, 30, 30, 30)
            drive.straight(-320)
            com.enviarMensagem("largarBolinhas")
            leiturasCorParede = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    wait(30)


