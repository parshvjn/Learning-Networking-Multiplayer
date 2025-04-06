import socket
from _thread import *
import sys
from utils import configs

server = configs.get('SERVER_IP').data
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("waiting for a connection, server started")

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1])

pos = [(0,0), (100, 100)]
def threaded_client(connection, player):
    connection.send(str.encode(make_pos(pos[player]))) #when conencting, should send some type of info to what we connected to (initial on-connecting msg)
    reply = ""
    while True:
        try:
            data = read_pos(connection.recv(2048).decode()) # 2048 is bits (amoutn of info we are tryinbg to recieve)
            pos[player] = data

            if not data: #if not getting any info
                print('Disconnected')
                break #disconnected from client
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print('Received:', data)
                print('Sending:', reply)
            
            connection.sendall(str.encode(make_pos(reply))) # when sending to client side, will need to decode again (i think for security)
        
        except:
            break
    print("lost connection")
    connection.close()
    #fix: when oen client disconnects and joins again, currentPlayer variable still adds one more and make index out of range error for finding the position when given to function (trheaded_client)


currentPlayer = 0
while True:
    connection, address = s.accept()
    print('Connected to:', address) #i think address is IP address

    start_new_thread(threaded_client, (connection, currentPlayer))
    currentPlayer += 1