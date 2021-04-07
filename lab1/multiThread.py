import threading
from socket import *

class ClientThread(threading.Thread): #Thay ko chua cai multithread nen ko biet dung hay sai

    def __init__(self, connect, address):
        threading.Thread.__init__(self)
        self.connectionSocket = connect
        self.addr = address

    def run(self):
        while True:
            try:
                message = self.connectionSocket.recv(1024).decode()
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
                else:
                    print(" ERROR: ", message)
            except IOError:
                connectionSocket.send(
                    'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<!doctype html><html><body><h1>404 Not Found<h1></body></html>'.encode())
                connectionSocket.close()
            finally:
                break

if __name__ == '__main__':
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverPort = 80
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)

    threads = []
    while True:
        print('Ready to serve ...')
        connectionSocket, addr = serverSocket.accept()

        clientThread = ClientThread(connectionSocket, addr)
        clientThread.setDaemon(True)  # The entire Python program exits when only daemon threads are left.
        clientThread.start()
        threads.append(clientThread)
        clientThread.join()