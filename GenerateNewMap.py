from Constantes import *
from random import random
import pygame
from pygame.locals import *



def ecrire(chaine):
    fichier = open("map.txt", "w")
    fichier.write(chaine)
    fichier.close()

class Case:
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.mur = True
        
    def car(self):
        if self.mur:
            return '#'
        else:
            return ' '


class Laby:
    
    def __init__(self):
        self.map = []
        fichier = open("map.txt")
        rawData = fichier.readlines()
        fichier.close()
        for l in range(len(rawData)):
            ligne = []
            for c in range(len(rawData[0])):
                m = Case(c, l)
                if rawData[l][c] == ' ':
                    m.mur = False
                ligne.append(m)
            self.map.append(ligne)

        print("Map loaded")

                    
    def newMap(self):
        self.map = []
        for i in range(LINES):
            liste = []
            for j in range(COLS):
                liste.append(Case(j,i))
            self.map.append(liste)
        self.vider()
        
                
    def create_spawns(self, taille):
        for i in range(1, taille+1):
            for j in range(1, taille+1):
                self.map[i][j].mur = False
        for i in range(LINES - taille-1, LINES-1):
            for j in range(COLS- taille-1, COLS-1):
                self.map[i][j].mur = False

    def vider(self):#Non utilisé
        for i in range(1, LINES-1):
            for j in range(1, COLS-1):
                self.map[i][j].mur = not self.map[i][j].mur

    def pr(self):
        chaine = ""
        for ligne in self.map:
            for mur in ligne:
                chaine += mur.car()
            chaine += '\n'
        return chaine

    def afficher(self, fenetre):
        fenetre.fill((255,255,255))
        for ligne in self.map:
            for mur in ligne:
                if mur.mur:
                    pygame.draw.rect(fenetre, (0,0,255), (mur.x*BLOC_SIZE, mur.y*BLOC_SIZE, BLOC_SIZE, BLOC_SIZE))
                                

    def main(self):
        fenetre = pygame.display.set_mode((COLS*BLOC_SIZE, LINES*BLOC_SIZE))
        pygame.display.set_caption("YERAK - LEVEL EDITOR")
        while True:
            self.afficher(fenetre)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    ordonne = event.pos[1]
                    abscisse = event.pos[0]
                    if self.map[ordonne // BLOC_SIZE][abscisse // BLOC_SIZE].mur:
                        self.map[ordonne // BLOC_SIZE][abscisse // BLOC_SIZE].mur = False
                    else:
                        self.map[ordonne // BLOC_SIZE][abscisse // BLOC_SIZE].mur = True

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.newMap()
                        print("New map")
                    elif event.key == K_RETURN:
                        ecrire(self.pr())
                        print("Map saved")
                    
                if event.type == QUIT:
                    exit()

def main():
    print("YERAK - LEVEL EDITOR")
    print("USE: \n   SPACE --> new map\n   ENTER --> save map")
    laby = Laby()
    laby.create_spawns(7)
    laby.main()



main()
