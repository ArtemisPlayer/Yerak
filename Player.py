from Constantes import *
from Objets import *
import pygame
import socket
import pickle
import time

from pygame.locals import *

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
            new_rect.posy += dy_correction*1.01
            new_rect.posx += dx_correction*1.01
    x, y = new_rect.posx, new_rect.posy
    return x, y, VX, VY

class Entity:
    def __init__(self, servIP, port = SERV_PORT):

        self.IP = servIP
        self.port = port
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
                pygame.draw.rect(fenetre, COLOR_W, (ent[2], ent[3], BLOC_SIZE, BLOC_SIZE))
            elif ent[4] == 'missile':
                pygame.draw.rect(fenetre, COLOR_MISSILE, (ent[2], ent[3], MISSILE_SIZE, MISSILE_SIZE))
        pygame.draw.rect(fenetre, COLOR_P, (self.posx,self.posy, BLOC_SIZE, BLOC_SIZE))



def player(SERV_IP):
    print("Tentative de connexion à " + SERV_IP + ":" + str(SERV_PORT))
    me = Entity(SERV_IP)
    me.connect()

    carte = Map("map.txt")

    fenetre = pygame.display.set_mode((carte.COLS*BLOC_SIZE, carte.LINES*BLOC_SIZE))
    last_launched = time.time()

    aff_time = time.time()
    masque = pygame.image.load("masque.png")
    masque = masque.convert_alpha()
    masque = pygame.transform.scale(masque, (LUM,LUM))
    while True:
        me.communicate()
        me.checkMissiles(last_launched)
        me.move(carte)

        ##séquence d'affichage

        if time.time() - aff_time > 0.005:
            fenetre.fill(COLOR_BG)
            fenetre.blit(masque, (me.posx - LUM//2 + BLOC_SIZE //2,me.posy - LUM//2 + BLOC_SIZE //2))
            pygame.draw.rect(fenetre, COLOR_W, (me.posx + LUM//2, me.posy - LUM//2, 2000, 2000))
            pygame.draw.rect(fenetre, COLOR_W, (me.posx - LUM//2 - 2000, me.posy - LUM//2 - 2000, 4000, 2020))
            pygame.draw.rect(fenetre, COLOR_W, (me.posx - LUM//2 - 2000, me.posy - LUM//2, 2020, 4000))
            pygame.draw.rect(fenetre, COLOR_W, (me.posx - LUM//2, me.posy + LUM//2, 2000, 2000))
            carte.afficher(fenetre, me.posx, me.posy)
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
