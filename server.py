import socket
import threading

# find IP address (ONLY FOR LOCAL HOSTING)
# ipFinder = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# ipFinder.connect(("1.1.1.1", 8080))
# ipAddress = ipFinder.getsockname()[0]
# ipFinder.close()
ipAddress = ""

# set up server
port = 5050
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ipAddress, port))

# multiprocessing to handle each client
headerSize = 32 # number of bits in message length
newMessages = []

class MessageObj:
    def __init__(self, length, message):
        self.length = length
        self.message = message

def receive_client(client, address, index):
    while True:
        msgLenBinary = client.recv(headerSize)
        if msgLenBinary:
            msgLen = int(msgLenBinary, 2)
            message = client.recv(msgLen)
            msgObj = MessageObj(msgLen, message)
            for i in range(len(newMessages)):
                newMessages[i].append(msgObj)
            print(f"Received Message from Client #{index}: {message.decode()}")
    client.close()
        
def send_client(client, address, index):
    # server.connect((address, port))
    while True:
        if newMessages[index]:
            msgObjects = newMessages[index]
            msgObj = msgObjects.pop(0)
            msgLen = bin(msgObj.length)[2:]
            msgLen = "0" * (headerSize - len(msgLen)) + msgLen
            message = msgObj.message
            client.send(msgLen.encode())
            client.send(message)
    client.close()

# main loop
print("Starting Server...")
numConnections = 0
server.listen()
while True:
    client, address = server.accept()
    newMessages.append([])
    recvThread = threading.Thread(target = receive_client, args = (client, address, numConnections))
    sendThread = threading.Thread(target = send_client, args = (client, address, numConnections))
    recvThread.start()
    sendThread.start()
    numConnections += 1
    print(f"Number of Clients Connected: {numConnections}")

