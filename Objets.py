from Constantes import *
import pygame
import time
from math import sqrt

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


class Wall:
    def __init__(self, x, y, health = float('inf'), color = COLOR_W):
        self.posx = x
        self.posy = y
        self.health = health
        self.color = COLOR_W
    
    def afficher(self, fenetre):
        pygame.draw.rect(fenetre, COLOR_W, (self.posx,self.posy, BLOC_SIZE, BLOC_SIZE))


class Missile:
    def __init__(self, tireur, x, y): #class cube pour tireur 
        self.posx = tireur.posx
        self.posy = tireur.posy
        hypo = sqrt((x-self.posx)**2+(y-self.posy)**2)
        self.vx = (x-self.posx)/hypo*MISSILE_SPEED
        self.vy = (y-self.posy)/hypo*MISSILE_SPEED
        self.type = 'missile'

    def move(self, last_update):
        self.posx += self.vx*(time.time()-last_update)
        self.posy += self.vy*(time.time()-last_update)


class Cube:
    def __init__(self, IP, connexion, name, posx, posy):
        self.IP = IP
        self.connexion = connexion
        self.posx = posx
        self.posy = posy
        self.vx = 0
        self.vy = 0
        self.last_update = time.time()
        self.nClient = name
        self.dead = False
        self.type = 'player'

    def move(self, last_update):
        #self.posx += self.vx*(time.time()-last_update)
        #self.posy += self.vy*(time.time()-last_update)
        pass


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
