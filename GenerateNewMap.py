from Constantes import *
from random import random


carte = ""

for i in range(COLS):
    carte += '#'

carte += '\n'

for i in range(1, LINES-1):
    carte += '#'
    for j in range(1, COLS-1):
        if random() > SEED:
            carte += '#'
        else:
            carte += ' '
    carte += '#\n'

for i in range(COLS):
    carte += '#'

print(carte)

fichier = open("map.txt", "w")
fichier.write(carte)
fichier.close()
