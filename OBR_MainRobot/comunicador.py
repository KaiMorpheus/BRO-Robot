#!/usr/bin/env pybricks-micropython

# Antes de executar este programa, certifique-se de que os 
# blocos EV3 do cliente e do servidor estejam emparelhados 
# usando Bluetooth, mas NÃO os conecte. O programa se encarregará 
# de estabelecer a conexão.

# O servidor deve ser iniciado antes do cliente!
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.messaging import BluetoothMailboxServer, BluetoothMailboxClient, TextMailbox
import threading

mensagens = ["vazio"] 

class Comunicador(threading.Thread):
    
    ev3 = 0
    isServidor = False
    mbox = None


    def __init__(self, ev3, isServidor):
        super().__init__
        
        threading.Thread.daemon = True
        self.ev3 = ev3
        self.isServidor = isServidor

    def ultimaMensagem(self) :
        return mensagens[-1]

    def run(self):
        global mensagens
        SERVER = 'ev3dev'

        if self.isServidor :
            comunicacao = BluetoothMailboxServer()
            self.mbox = TextMailbox('mensagens', comunicacao)
            self.ev3.screen.print('Servidor iniciado', sep=' ', end='\n')
            self.ev3.screen.print('Aguardando conexao', sep=' ', end='\n')
            comunicacao.wait_for_connection()
            self.ev3.screen.print('Conectado', sep=' ', end='\n')
        else :
            comunicacao = BluetoothMailboxClient()
            self.mbox = TextMailbox('mensagens', comunicacao)
            self.ev3.screen.print('Cliente iniciado', sep=' ', end='\n')
            self.ev3.screen.print('Conectando ao servidor', sep=' ', end='\n')
            comunicacao.connect(SERVER)
            self.ev3.screen.print('Conectado', sep=' ', end='\n')
        
        while True:
            self.mbox.wait()
            mensagens.append(self.mbox.read())

    def enviarMensagem(self,mensagem) :
        self.mbox.send(mensagem)