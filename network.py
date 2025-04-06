import socket
from utils import configs

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = configs.get('SERVER_IP')
        self.port = 5555
        self.address = (self.server, self.port)
        self.pos = self.connect()
    
    def getPos(self):
        return self.pos
    
    def connect(self):
        try:
            self.client.connect(self.address)
            return self.client.recv(2048).decode()
        except:
            return False
    
    def send(self,data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)