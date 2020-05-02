import socket
import pickle
import time
import pygame
from pygame.locals import *

SERV_IP = input('IP serveur >>> ')

if SERV_IP == '':
    SERV_IP, SERV_PORT, FREIN = 'localhost', 12000, 50
else:
    SERV_PORT = int(input('Port serveur >>> '))
    FREIN = float(input('50 est bien : '))


SIZE = 700
COLOR_BG = (255,255,255)
COLOR_P1 = (0,0,0)
COLOR_P = (0,0,200)
SPEED = 150

class Entity:
    def __init__(self, servIP = SERV_IP, port = SERV_PORT):
        self.IP = servIP
        self.port = port
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.posx = 0.
        self.posy = 0.
        self.vx = 0.
        self.vy = 0.
        self.world = []

    def connect(self):
        counter = 0
        while True:
            try:
                self.connexion.connect((self.IP, self.port))
                print('Connexion établie !')
                break
            except:
                counter += 1
                print('Echec de la connexion, lors de la tentative '+str(counter))
    
    def communicate(self):
        #le client envoie :[vx, vy]
        #et reçoit: [nb_player, id_player, [px, py], ...]
        self.connexion.send(pickle.dumps([self.vx, self.vy]))
        recu = self.connexion.recv(1024)
        self.world = pickle.loads(recu)

    def afficher(self, fenetre):
        fenetre.fill(COLOR_BG)
        nc = self.world[1]
        nbp = self.world[0]
        for i in range(2, nbp+2):
            if i-2 == nc:
                pygame.draw.rect(fenetre, COLOR_P1, (self.world[i][0],self.world[i][1], 6, 6))
            else:
                pygame.draw.rect(fenetre, COLOR_P, (self.world[i][0],self.world[i][1], 6, 6))
      

def main():
    print("Tentative de connexion à " + SERV_IP + ":" + str(SERV_PORT))
    me = Entity()
    me.connect()
    fenetre = pygame.display.set_mode((SIZE, SIZE))
    last_updated = time.time()
    while True:
        me.communicate()
        me.afficher(fenetre)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                while True:
                    me.connexion.send(b'fin')
                    time.sleep(0.2)
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    me.vy = -SPEED
                if event.key == K_DOWN:
                    me.vy = SPEED
                if event.key == K_LEFT:
                    me.vx = -SPEED
                if event.key == K_RIGHT:
                    me.vx = SPEED


        if me.vx >= 0:
            me.vx = max(me.vx - FREIN*(time.time()-last_updated), 0)
        else:
            me.vx = min(me.vx + FREIN*(time.time()-last_updated), 0)

        if me.vy >= 0:
            me.vy = max(me.vy - FREIN*(time.time()-last_updated), 0)
        else:
            me.vy = min(me.vy + FREIN*(time.time()-last_updated), 0)

        last_updated = time.time()






main()
