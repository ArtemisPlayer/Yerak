import socket

SERV_PORT = 12000 #Port du serveur
TIMEOUT = 0.0
CONN_TYPE = socket.AF_INET #socket.AF_INET6 si IPv6

FREIN = 300.0  #Ralenti chaque joueur
ACCELERATION = 2200  #Accelere chaque joueur
SPEED = 300  #Vitesse max
MISSILE_SPEED = 0.01

COLOR_BG = (255,255,255) #Couleur de l'arriere plan
COLOR_P1 = (0,0,0) #Couleur des autres
COLOR_P = (0,0,200)  #Couleur de soi
COLOR_W = (40,40,40) #Couleur des murs et des ombres
COLOR_MISSILE = (230,0,0) #Couleur des missiles

BLOC_SIZE = 14 #Taille des blocs en pixels
MISSILE_SIZE = 5 #Taille des missiles
SIZE = 100

CADENCE = 1.0 #Cadence de tir


LINES = 41 #dimensions de la map pour eviter de calculer les ombres des murs
COLS = 81

SEED = 0.92  #densité de blocs sur la map

LUM = 600 #augmente avec l'éclairage
