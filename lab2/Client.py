from socket import *
import time

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)
try:
    clientSocket.connect((serverName, serverPort))
    for i in range(10):
        start = time.time()
        message = "Ping #" + str(i)
        try:
            clientSocket.send(message.encode())
            print("Sended", message)
            respond = clientSocket.recv(1024)
            print("Received", respond.decode())
            end = time.time()
            print("RTT: "+ str(end-start), " from ", start, "to", end, "second\n")
        except timeout:
            print("#" + str(i), "Requested time out\n")
finally:
    clientSocket.close()