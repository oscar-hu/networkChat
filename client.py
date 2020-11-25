import socket
import threading

serverIP = ""
port = 5050
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((serverIP, port))
headerSize = 32

def send_server(name):
    print("[TYPE MESSAGE BELOW]")
    while True:
        message = (name + ': ' + input())
        print("\033[A                             \033[A") # removes text that was just written
        msgLen = bin(len(message))[2:]
        msgLen = "0" * (headerSize - len(msgLen)) + msgLen
        client.send(msgLen.encode())
        client.send(message.encode())

def from_server():
    while True:
        msgLenBinary = client.recv(headerSize)
        if msgLenBinary:
            msgLen = int(msgLenBinary, 2)
            message = client.recv(msgLen).decode()
            print(message)
        
name = input("Enter your name: ")
recvThread = threading.Thread(target = from_server)
sendThread = threading.Thread(target = send_server, args = (name,))
recvThread.start()
sendThread.start()

