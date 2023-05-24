import socket
import threading
from time import sleep
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)
connected = True

def handle_rev(client):
    global connected
    while connected:
        msg = client.recv(1024).decode(FORMAT)
        print("\n"+ msg)
        print("\nC02>")
       # print(len(msg))

def handle_send(client):
    global connected
    while connected:
        msg = input("C02>")
        send("[Client 02]  " + msg)
        if msg == DISCONNECT_MESSAGE:
            connected = False

def send(msg):
    message = msg.encode(FORMAT)
    message+= b' ' * (30 - len(message))
    client.send(message)
thead = threading.Thread(target=handle_rev,args=(client,))
thead.start()
thead = threading.Thread(target=handle_send,args=(client,))
thead.start()
while connected:
    sleep(2)