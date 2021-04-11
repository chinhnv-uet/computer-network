from socket import *
import time

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

minRTT, maxRTT = 99999, 0
sumRTT = 0
countLoss = 0

try:
    clientSocket.connect((serverName, serverPort))
    for i in range(10):
        start = time.time()
        message = "Ping #" + str(i)
        try:
            clientSocket.send(message.encode())
            respond = clientSocket.recv(1024)
            print("Received", respond.decode())

            end = time.time()
            RTT = end - start
            minRTT = str(min(float(minRTT), RTT))
            maxRTT = str(max(float(maxRTT), RTT))
            sumRTT += RTT

            print("RTT: " + str(RTT), " from ", start, "to", end, "second\n")
        except timeout:
            countLoss += 1
            print("#" + str(i), "Requested time out\n")
finally:
    clientSocket.close()
print('_' * 30)
print("\nMin RTT = %s, Max RTT = %s" % (minRTT, maxRTT))
print("Packet loss rate", (countLoss/10))
print("Averange RTTs:", (sumRTT / (10 - countLoss)))
