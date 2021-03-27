from socket import *
import sys  # read argument if run by CMD

if __name__ == '__main__':
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])
    fileName = sys.argv[3]

    clientSocket = socket(AF_INET, SOCK_STREAM)

    try:
        clientSocket.connect((serverName, serverPort))
        message = 'Get /' + sys.argv[3]

        clientSocket.send(message.encode())
        sentence = clientSocket.recv(1024, MSG_WAITALL)  # Neu ko co flag thi chi nhan dc 200 Ok ko nhan dc may cai con lai va se xay ra error
        print(sentence.decode())

    except IOError:
        sys.exit()
    clientSocket.close()
    # client.py 192.168.98.102 6789 index.html
