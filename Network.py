import socket
import pickle
import time
import pygame
from pygame.locals import *
from math import floor

SERV_IP = input('IP serveur >>> ')

if SERV_IP == '':
    SERV_IP, SERV_PORT, FREIN = 'localhost', 12000, 300
else:
    SERV_PORT = int(input('Port serveur >>> '))
    FREIN = float(input('50 est bien : '))



ACCELERATION = 2200
COLOR_BG = (255,255,255)
COLOR_P1 = (0,0,0)
COLOR_P = (0,0,200)
SPEED = 500
COLOR_W = (40,40,40)
BLOC_SIZE = 15
MISSILE_SPEED = 0.0005
MISSILE_SIZE = 5
COLOR_MISSILE = (230,0,0)
CADENCE = 1.0

class rectangle:#obligé de recoder pygame n'aime pas les float
    def __init__(self, x, y, largeur, hauteur):
        self.posx = x
        self.posy = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.top = y
        self.bottom = y + hauteur
        self.left = x
        self.right = x + largeur
    
    def contient(self, x, y):
        return self.bottom >= y >= self.top and self.right >= x >= self.left

    def colliderect(self, autre):
        return (self.contient(autre.posx, autre.posy) or self.contient(autre.posx+BLOC_SIZE, autre.posy) 
                    or self.contient(autre.posx+BLOC_SIZE, autre.posy) or self.contient(autre.posx+BLOC_SIZE, autre.posy+BLOC_SIZE))


def compute_penetration(block, old_rect, new_rect):
    dx_correction = dy_correction = 0.0
    if old_rect.bottom <= block.top < new_rect.bottom:
        dy_correction = block.top  - new_rect.bottom
    elif old_rect.top >= block.bottom > new_rect.top:
        dy_correction = block.bottom - new_rect.top
    if old_rect.right <= block.left < new_rect.right:
        dx_correction = block.left - new_rect.right
    elif old_rect.left >= block.right > new_rect.left:
        dx_correction = block.right - new_rect.left
    return dx_correction, dy_correction

def bloque_sur_collision(map, old_pos, new_pos, v0x, v0y):
    old_rect = rectangle(old_pos[0], old_pos[1], BLOC_SIZE, BLOC_SIZE)
    new_rect = rectangle(new_pos[0], new_pos[1], BLOC_SIZE, BLOC_SIZE)
    VX = v0x
    VY = v0y
    for block in map.detect(new_pos[0], new_pos[1]):
        R = rectangle(block.posx, block.posy, BLOC_SIZE, BLOC_SIZE)
        if new_rect.colliderect(R):
            dx_correction, dy_correction = compute_penetration(R, old_rect, new_rect)
            if dx_correction != 0. :
                VX = 0
            if dy_correction != 0. :
                VY = 0
            new_rect.posy += dy_correction
            new_rect.posx += dx_correction
    x, y = new_rect.posx, new_rect.posy
    return x, y, VX, VY

class Wall:
    def __init__(self, x, y, health = float('inf'), color = COLOR_W):
        self.posx = x
        self.posy = y
        self.health = health
        self.color = COLOR_W
    
    def afficher(self, fenetre):
        pygame.draw.rect(fenetre, COLOR_W, (self.posx,self.posy, BLOC_SIZE, BLOC_SIZE))

class Map:  
    def __init__(self, path):
        fichier = open(path, 'r')
        raw = fichier.read()
        fichier.close()
        self.map = []
        i, j = 0, 0
        self.LINES, self.COLS = -1, -1
        for car in raw:
            if car == '#':
                self.map.append(Wall(i*BLOC_SIZE, j*BLOC_SIZE))
            if car == '\n':
                if j == 0:
                    self.COLS = i
                i = 0
                j += 1
            else:
                i += 1
        self.LINES = j + 1

    def afficher(self, fenetre):
        for w in self.map:
            w.afficher(fenetre)
    
    def detect(self, x, y):
        toCheck = []
        for mur in self.map:
            if abs(mur.posx - x) > 2*BLOC_SIZE or abs(mur.posy - y) > 2*BLOC_SIZE:
                pass #pour utiliser l'optimisation du or en python
            else:
                toCheck.append(mur)
        return toCheck

class Entity:
    def __init__(self, servIP = SERV_IP, port = SERV_PORT):

        self.IP = servIP
        self.port = port
        self.connexion = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        self.posx = 20.
        self.posy = 20.
        self.vx = 0.
        self.vy = 0.
        self.accx = 0.
        self.accy = 0.
        self.world = []
        self.last_update = time.time()

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
        #le client envoie :[vx, vy, posx, posy, type, sante, nom]
        #et reçoit: [nb_entites, id_player, [vx, vy, posx, posy, type], ...]
        #ou [nb_entites, id_player, [vx, vy, posx, posy, type], ...]
        #avec type = missile ou joueur

        self.connexion.send(pickle.dumps([self.vx, self.vy, self.posx, self.posy]))
        recu = self.connexion.recv(2048)
        self.world = pickle.loads(recu)

    def move(self, carte):
        delta = time.time() - self.last_update
        for coord in self.world[2:]:
            coord[2] += coord[0]*delta
            coord[3] += coord[1]*delta
        
        if self.vx >= 0:
            self.vx = min(self.accx*delta + self.vx, SPEED)
        else:
            self.vx = max(self.accx*delta + self.vx, -SPEED)

        if self.vy >= 0:
            self.vy = min(self.accy*delta + self.vy, SPEED)
        else:
            self.vy = max(self.accy*delta + self.vy, -SPEED)

        if self.vx >= 0:
            self.vx = max(self.vx - FREIN*delta, 0)
        else:
            self.vx = min(self.vx + FREIN*delta, 0)

        if self.vy >= 0:
            self.vy = max(self.vy - FREIN*delta, 0)
        else:
            self.vy = min(self.vy + FREIN*delta, 0)

        old_pos = [self.posx, self.posy]
        new_pos = [self.vx*delta + self.posx, self.vy*delta + self.posy]

        self.posx, self.posy, self.vx, self.vy = bloque_sur_collision(carte, old_pos, new_pos, self.vx, self.vy)
        self.last_update = time.time()

    def checkMissiles(self, last_launched):
        liste = []
        for ent in self.world[2:]:
            if ent[4] == 'missile':
                liste.append(ent)
        if time.time() - last_launched < 0.5:
            return None
        for miss in liste:
            if rectangle(self.posx, self.posy, BLOC_SIZE, BLOC_SIZE).colliderect(rectangle(miss[2], miss[3], 1, 1)):
                self.vx = self.vy = 0
                self.posx = self.posy = 20
                ind = self.world[2:].index(miss)
                self.connexion.send(pickle.dumps(['destroy', ind]))
                print("Perdu !")
                input()
                exit(0)
                break

    def afficher(self, fenetre):
        #fenetre.fill(COLOR_BG)
        nc = self.world[1] #######
        nbp = self.world[0]
        for ent in self.world[2:]:
            if ent[4] == 'player':
                pygame.draw.rect(fenetre, COLOR_P1, (ent[2], ent[3], BLOC_SIZE, BLOC_SIZE))
            elif ent[4] == 'missile':
                pygame.draw.rect(fenetre, COLOR_MISSILE, (ent[2], ent[3], MISSILE_SIZE, MISSILE_SIZE))
        pygame.draw.rect(fenetre, COLOR_P, (self.posx,self.posy, BLOC_SIZE, BLOC_SIZE))
      

def main():
    print("Tentative de connexion à " + SERV_IP + ":" + str(SERV_PORT))
    me = Entity()
    me.connect()

    carte = Map("map.txt")

    fenetre = pygame.display.set_mode((carte.COLS*BLOC_SIZE, carte.LINES*BLOC_SIZE))
    last_launched = time.time()

    aff_time = time.time()
    
    while True:
        me.communicate()
        me.checkMissiles(last_launched)
        me.move(carte)

        ##séquence d'affichage

        if time.time() - aff_time > 0.005:
            fenetre.fill(COLOR_BG)
            carte.afficher(fenetre)
            me.afficher(fenetre)
            pygame.display.flip()
            aff_time = time.time()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                while True:
                    me.connexion.send(pickle.dumps(['fin']))
                    time.sleep(0.2)
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    while True:
                        me.connexion.send(pickle.dumps(['fin']))
                        time.sleep(0.2)

                
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            me.accy = -ACCELERATION
        elif keys[K_DOWN]:
            me.accy = ACCELERATION
        else:
            me.accy = 0

        if keys[K_LEFT]:
            me.accx = -ACCELERATION
        elif keys[K_RIGHT]:
            me.accx = ACCELERATION
        else:
            me.accx = 0

        if pygame.mouse.get_pressed()[0]: 
            if time.time() - last_launched > CADENCE:
                abscisse, ordonne = pygame.mouse.get_pos()
                me.connexion.send(pickle.dumps(['shoot', abscisse, ordonne]))
                last_launched = time.time()      
        
main()

