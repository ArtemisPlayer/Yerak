import socket
import select
import time
import pickle

SIZE = 100
TIMEOUT = 0.0

DEBUG = True

class Clients:
    def __init__(self):
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion.bind(('',12000))
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
            msg_recu = connClient.recv(1024)
        except ConnectionResetError:
            msg_recu = b'fin'
            
        if msg_recu == b'fin':
            connClient.close()
            self.clients_connectes[nClient].dead = True
            self.clients_connectes[nClient].vx = 0
            self.clients_connectes[nClient].vy = 0
            return None

        try:
            msg_recu = pickle.loads(msg_recu)
            bdata = pickle.dumps(data)
            connClient.send(bdata)
        except:
            print('pickle error, passing')

        return msg_recu

    def update(self):
        global DEBUG
        liste_pos = [[a.posx, a.posy] for a in self.clients_connectes]
        n = len(self.clients_connectes)
        for c in self.clients_connectes:
            reception = self.communicate(c.nClient, [n, c.nClient] + liste_pos)
            if reception != None:
                if DEBUG:
                    print(reception)
                    DEBUG = False

                try:
                    c.vx, c.vy = reception
                except:
                    print(reception)
    def run(self):
        self.accepter_new()
        self.update()
        for c in self.clients_connectes:
            c.move()


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

    def move(self):
        self.posx += self.vx*(time.time()-self.last_update)
        self.posy += self.vy*(time.time()-self.last_update)
        self.last_update = time.time()
    
def main():
    serv = Clients()
    while True:
        serv.run()

main()








