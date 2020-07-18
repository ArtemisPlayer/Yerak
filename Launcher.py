print("Starting...")

from Constantes import *
from Objets import *
from Serveur import *
from Player import *

from pygame.locals import *


def launcher():
    print("Hello !")
    print("USE: \n'server' to host or the IP adress of the server you want to join")
    SERV_IP = input("> ")

    if SERV_IP == 'server':     
        carte = Map("map.txt")
        serv = Clients()
        print("Server online !")
        last_update = time.time()
        while True:
            serv.run(last_update, carte)

    else:
        player(SERV_IP)

launcher()
