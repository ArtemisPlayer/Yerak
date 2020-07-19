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

    def ombre(self, fenetre, x0, y0):

        if self.posx == 0 or self.posy == 0 or self.posx == COLS*BLOC_SIZE or self.posy == LINES*BLOC_SIZE:
            return None
        xo = x0 + BLOC_SIZE//2
        yo = y0 + BLOC_SIZE//2
        
        d = sqrt((self.posx-xo)**2 + (self.posy-yo)**2)

        if d > 200:
            return None
        
        xi = self.posx + BLOC_SIZE//2
        yi = self.posy + BLOC_SIZE//2
        
        
        if xo < self.posx and yo < self.posy:
            x1, y1, x2, y2 = self.posx + BLOC_SIZE, self.posy, self.posx, self.posy + BLOC_SIZE

        elif self.posx <= xo < self.posx + BLOC_SIZE and yo < self.posy:
            x1, y1, x2, y2 = self.posx + BLOC_SIZE, self.posy, self.posx, self.posy 

        elif self.posx <= xo and yo < self.posy:
            x1, y1, x2, y2 = self.posx + BLOC_SIZE-1, self.posy + BLOC_SIZE, self.posx, self.posy 

        elif self.posx <= xo and self.posy <= yo < self.posy + BLOC_SIZE:
            x1, y1, x2, y2 = self.posx + BLOC_SIZE -1, self.posy + BLOC_SIZE, self.posx + BLOC_SIZE-1, self.posy-1

        elif self.posx + BLOC_SIZE <= xo and self.posy + BLOC_SIZE <= yo:
            x1, y1, x2, y2 = self.posx-1, self.posy + BLOC_SIZE-1, self.posx + BLOC_SIZE-1, self.posy-1

        elif self.posx <= xo < self.posx + BLOC_SIZE and self.posy + BLOC_SIZE <= yo:
            x1, y1, x2, y2 = self.posx-1, self.posy + BLOC_SIZE, self.posx + BLOC_SIZE, self.posy + BLOC_SIZE-1
                                                    #
        elif xo < self.posx and self.posy + BLOC_SIZE <= yo:
            x1, y1, x2, y2 = self.posx, self.posy-1, self.posx + BLOC_SIZE-1, self.posy + BLOC_SIZE-1

        else:
            x1, y1, x2, y2 = self.posx , self.posy-1, self.posx, self.posy + BLOC_SIZE
            
        d1 = sqrt((xo - x1)**2+(yo - y1)**2)
        d2 = sqrt((xo - x2)**2+(yo - y2)**2)
        x3 = (x2 - xo)/d2*2000 + x2
        y3 = (y2 - yo)/d2*2000 + y2
        x4 = (x1 - xo)/d1*2000 + x1
        y4 = (y1 - yo)/d1*2000 + y1
        pygame.draw.polygon(fenetre, COLOR_W, [(x1, y1), (x2,y2), (x3, y3), (x4, y4)])




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

    def afficher(self, fenetre, x, y):
        for w in self.map:
            w.afficher(fenetre)
            w.ombre(fenetre, x, y)
    
    def detect(self, x, y):
        toCheck = []
        for mur in self.map:
            if abs(mur.posx - x) > 2*BLOC_SIZE or abs(mur.posy - y) > 2*BLOC_SIZE:
                pass #pour utiliser l'optimisation du or en python
            else:
                toCheck.append(mur)
        return toCheck
