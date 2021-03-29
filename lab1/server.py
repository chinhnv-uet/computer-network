from socket import *
import sys

def server():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverPort = 6789
    serverSocket.bind(('', serverPort))
    serverSocket.listen(5)
    while True:
        print('Ready to serve ...')
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024).decode()
            if len(message) > 1:
                filename = message.split()[1]

                print(filename)

                f = open(filename[1:])
                outputdata = f.read()
                f.close()

                connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
                connectionSocket.send('Content-Type: text/html\n'.encode())

                connectionSocket.send('\n'.encode())
                for i in range(0, len(outputdata)):
                    connectionSocket.send(outputdata[i].encode())
                connectionSocket.send("\r\n".encode())

                connectionSocket.close()
        except IOError:
            connectionSocket.send('HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<!doctype html><html><body><h1>404 Not Found<h1></body></html>'.encode())
            connectionSocket.close()
    serverSocket.close()
    sys.exit()


if __name__ == '__main__':
    server()
