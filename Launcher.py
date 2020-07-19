
from Constantes import *
from Objets import *
from Serveur import *
from Player import *
import sys
import os

    
def clear(): 

    if os.name == 'nt': 
        os.system('cls') 
  
    else: 
        os.system('clear') 

def launcher():
    clear()
    if len(sys.argv) > 1:
        SERV_IP = 'server'
    else:
        print("YERAK - A (VERY) BASIC MULTIPLAYER GAME")
        print("USE: \n    'server' to host or the IP adress of the server you want to join")
        print("    '' (just press enter) for a local demo (no multiplayer)")
        SERV_IP = input("> ")

    if SERV_IP == 'server':
        carte = Map("map.txt")
        serv = Clients()
        print("Server online !")
        last_update = time.time()
        while True:
            serv.run(last_update, carte)
    elif SERV_IP == '':
        os.popen("python Launcher.py arg")
        #os.popen("Launcher.exe arg")
        #pour exe
        player('localhost')
    else:
        player(SERV_IP)

launcher()
