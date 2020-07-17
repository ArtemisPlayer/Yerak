import socket
import select
import time
import pickle
from math import sqrt

SIZE = 100
TIMEOUT = 0.0
PORT = 12000
MISSILE_SPEED = 0.0005



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



class Clients:
    def __init__(self):
        self.connexion = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.connexion.bind(('',PORT))
        self.clients_connectes = []
        self.connexion.listen(5)

    def accepter_new(self):
        connexions_demandees = select.select([self.connexion],[], [], TIMEOUT)[0]
        for conn in connexions_demandees:
            newConn, newInfos = conn.accept()
            self.clients_connectes.append(Cube(newInfos[0], newConn, len(self.clients_connectes), 0, 0))
            print('Nouvelle connexion : ' + str(newInfos))

    def communicate(self, nClient, data):
        if self.clients_connectes[nClient].dead:
            return None

        try:
            connClient = select.select([self.clients_connectes[nClient].connexion], [], [], TIMEOUT)[0]
        except select.error:
            return None
        if connClient == []:
            return None

        connClient = connClient[0]
        try:
            msg_recu = connClient.recv(2048)
        except ConnectionResetError:
            print('connexion reset error')
            msg_recu = ['fin']

        try:
            if msg_recu != ['fin']:
                msg_recu = pickle.loads(msg_recu)
        except:
            return None

        if msg_recu == ['fin']:
            connClient.close()
            self.clients_connectes[nClient].dead = True
            self.clients_connectes[nClient].vx = 0
            self.clients_connectes[nClient].vy = 0
            return None
        
        elif msg_recu[0] == 'shoot':
            self.clients_connectes.append(Missile(self.clients_connectes[nClient], msg_recu[1], msg_recu[2]))
            return None

        elif msg_recu[0] == 'destroy':
            self.clients_connectes[msg_recu[1]].vx = 0
            self.clients_connectes[msg_recu[1]].vy = 0
            self.clients_connectes[msg_recu[1]].posx = -50
            self.clients_connectes[msg_recu[1]].posy = -50
            return None
        
        bdata = pickle.dumps(data)
        connClient.send(bdata)

        return msg_recu

    def update(self):
        liste_send = [[a.vx, a.vy, a.posx, a.posy, a.type] for a in self.clients_connectes]
        n = len(self.clients_connectes)
        for c in self.clients_connectes:
            if c.type == 'player':
                reception = self.communicate(c.nClient, [n, c.nClient] + liste_send)
                if reception != None:
                    c.vx, c.vy, c.posx, c.posy = reception
   

    def run(self, last_update):
        self.accepter_new()
        self.checkMis()
        self.update()
        for c in self.clients_connectes:
            c.move(last_update)
        last_update = time.time()

    def checkMis(self):
        for i in range(len(self.clients_connectes)):
            if self.clients_connectes[i].type == 'missile':
                if abs(self.clients_connectes[i].posx) + abs(self.clients_connectes[i].posy) > 1000:
                    del self.clients_connectes[i]
                    break

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
    
    
def main():
    serv = Clients()
    last_update = time.time()
    while True:
        serv.run(last_update)



main()








