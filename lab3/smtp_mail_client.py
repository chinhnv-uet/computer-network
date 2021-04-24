from socket import *
import ssl      #dung cho gmal.com de dam bao bao mat thong tin dang nhap
import base64
#TODO: source: https://github.com/Vishnu-Adda/gold-team-hw3/blob/master/mail_client.py
#TODO: tham khao may bai co dung ssl:   (https://github.com/ruizhu5100/CMPE-148-Lab-03/blob/main/mailclient.py)
            #https://github.com/khtr9490/SMTP-LAB-python-3.8/blob/main/main.py
#TODO: co anh:  #https://github.com/tim-kao/Computer-Network-Lab3-SMTP-Client-Socket-Programming-with-Python3/blob/main/smtp.py

msg = "\r\n I love Computer Networks"
endmsg = "\r\n.\r\n"

mailserver = ("smtp.gmail.com", 587)    #use for gmail

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)    #Ket noi socket voi mail server

recv = clientSocket.recv(1024).decode()
print("After connection request: " + recv)
if recv[:3] != '220':  # 220 server is ready for a new client
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print('recv1:', recv1)
if recv1[:3] != '250':  # 250 bieu thi viec gui message da duoc hoan thanh
    print('250 reply not received from server.')

#Send START TLS command
tlsCommand = 'STARTTLS\r\n'
clientSocket.send(tlsCommand.encode())
tlsRecv = clientSocket.recv(1024).decode()
print('tls receive:', tlsRecv)
if tlsRecv[:3] != '220':
    print('220 reply not received from server')

#Add SSL
clientSocket = ssl.wrap_socket(clientSocket)

#Send HELO again
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print('Receive after send HELO again', recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

#Send AUTH login command
authCommand = 'AUTH LOGIN\r\n'
clientSocket.send(authCommand.encode())
authRecv = clientSocket.recv(1024).decode()
print('After send AUTH command:', authRecv)
if authRecv[:3] != '334':
    print('334 reply not received from server.')

#Send username in base 64
username = 'nchinh219@gmail.com'
encodeUsername = base64.b64encode(username.encode())
stringUsername = str(encodeUsername, "utf-8") + '\r\n'
clientSocket.send(stringUsername.encode())
userRecv = clientSocket.recv(1024).decode()
print('After send username: ', userRecv)
if userRecv[:3] != '334':
    print('334 reply not received from server.')

#Send password in base 64
password = 'superpassword123@'
encodePassword = base64.b64encode(password.encode())
stringPassword = str(encodePassword, "utf-8") + '\r\n'
clientSocket.send(stringPassword.encode())
passRecv = clientSocket.recv(1024).decode()
print('After send password: ', passRecv)
if passRecv[:3] != '235':
    print('235 reply not received from server.')

# Send MAIL FROM command and print server response.
sender = '<chinhLtt>'
mailFromCommand = 'MAIL FROM: ' + sender +'\r\n'
clientSocket.send(mailFromCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print('Recv2', recv2)
if recv2[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.
recipent = '<nchinh2609@gmail.com>'
rcptToCommand = 'RCPT TO: ' + recipent + '\r\n'
clientSocket.send(rcptToCommand.encode())
recv3 = clientSocket.recv(1024).decode()
print('Recv3', recv3)
if recv3[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
recv4 = clientSocket.recv(1024).decode()
print('recv4:', recv4)
if recv4[:3] != '354':
    print('354 reply not received from server.')

# Send message data.
clientSocket.send(msg.encode())

#Message end with a single period.
clientSocket.send(endmsg.encode())
recv5 = clientSocket.recv(1024).decode()
print('recv5:', recv5)
if recv5[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
recv6 = clientSocket.recv(1024).decode()
print('recv6', recv6)
if recv6[:3] != '221':
    print('221 reply not received from server.')
print('send message successfully')
#close socket after send QUIT
clientSocket.close()
