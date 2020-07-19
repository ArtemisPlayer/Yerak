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
        for i in range(LINES):
            liste = []
            for j in range(COLS):
                liste.append(Case(j,i))
            self.map.append(liste)
                
    def create_spawns(self, taille):
        for i in range(1, taille+1):
            for j in range(1, taille+1):
                self.map[i][j].mur = False
        for i in range(LINES - taille-1, LINES-1):
            for j in range(COLS- taille-1, COLS-1):
                self.map[i][j].mur = False

    def vider(self):
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
        pygame.display.set_caption("Yerak - EDITEUR DE NIVEAU")
        print(self.pr())
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
                if event.type == QUIT:
                    ecrire(self.pr())
                    exit()

def main():
    laby = Laby()
    laby.create_spawns(7)
    laby.vider()
    laby.main()



main()
