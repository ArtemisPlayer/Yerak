from Constantes import *
from Serveur import *

print("YERAK - A (VERY) BASIC MULTIPLAYER GAME")
print("NO PYGAME SERVER ONLY VERSION")
carte = Map("map.txt")
serv = Clients()
print("Server online !")
last_update = time.time()
while True:
    serv.run(last_update, carte)
