import random as rd
from socket import *

#Create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 12000))

while True:
    print('ready to serve ...')
    #Generate random number in range of 0 to 10
    rand = rd.randint(0, 10)
    #Receive the client packet along with the address it is comming from
    message, address = serverSocket.recvfrom(1024)
    #Capitalize the message from the client
    message = message.upper()
    #if rand is less than 4, we consider the packet lost and do not respond
    if rand < 4:
        continue
    #otherwise, the server respond
    serverSocket.sendto(message, address)


