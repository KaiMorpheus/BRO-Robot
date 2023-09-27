#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.media.ev3dev import Font

from comunicador import *

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.
ev3 = EV3Brick()
ev3.screen.set_font(Font(size=10))



giroscopioHorizontal = GyroSensor(Port.S2)
giroscopioVertical = GyroSensor(Port.S1)
motorDesceBolinhas = Motor(Port.D)
segundoMotorGarra = Motor(Port.C)
comecaSegundaParte = False 
# Create your objects here.



# Write your program here.
ev3.speaker.beep()
#comunicador.iniciarServidor(ev3)
#comunicador.iniciarCliente(ev3)
comecouSubir = False
isServidor = False
memoriaAbreGarra = False
#com = Comunicador(ev3, False)
#com.start()
leituraHorizontal = 0
leituraVertical = 0
memoriaTerminaAbreGarra = False
memoriaFechaGarra = False
memoriaReset = False

    #CLIENTE
com = Comunicador(ev3, False)
com.start()
wait(5000)
com.enviarMensagem('comece')


ev3.screen.print(mensagens[-1], sep=' ', end='\n')
motorDesceBolinhas.run_angle(50, 1, then=Stop.HOLD, wait=True)
while True :

    print (leituraHorizontal)

    leituraVertical = giroscopioVertical.angle()
    leituraHorizontal = giroscopioHorizontal.angle()


    if (leituraVertical >= 8 and comecouSubir == False):
        com.enviarMensagem('rampa')
        comecouSubir = True

    if (leituraVertical < 8 and comecouSubir == True):
        comecouSubir = False
        com.enviarMensagem('terminouRampa')
        comecaSegundaParte = True
    
    if (leituraHorizontal > 205 and comecaSegundaParte == True):
        comecaSegundaParte = False
        com.enviarMensagem('terminouVolta')


    if(com.ultimaMensagem() == "resetaAngulo" and memoriaReset == False):
        giroscopioHorizontal.reset_angle(0)
        print("resetou")
        memoriaReset = True

    if (com.ultimaMensagem() == 'terminaAbreGarra') and (memoriaTerminaAbreGarra == False):
        segundoMotorGarra.run_angle(40, 30, then=Stop.HOLD, wait=True)
        memoriaTerminaAbreGarra = True


    if(com.ultimaMensagem() == 'FechaGarra') and (memoriaFechaGarra == False):
        segundoMotorGarra.run_angle(40, -150, then=Stop.HOLD, wait=True)
        memoriaFechaGarra = True

    if(com.ultimaMensagem() == 'largarBolinhas'):
        motorDesceBolinhas.run_angle(50, -70, then=Stop.HOLD, wait=True)

    if ((com.ultimaMensagem() == 'abreGarra') and (memoriaAbreGarra == False)):
        memoriaAbreGarra = True
        segundoMotorGarra.run_angle(100, 120, then=Stop.HOLD, wait=True)






