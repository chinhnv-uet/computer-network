from socket import *
import ssl  # dung cho gmal.com de dam bao bao mat thong tin dang nhap
import base64

USERNAME = 'nchinh219@gmail.com'
sender = USERNAME
PASSWORD = 'superpassword123@'
RECIPENT = 'nchinh2609@gmail.com'
subjectEmail = "Test send email with image"
msg = "\r\n I share my picture with you."

# Load image
filename = "autumn-theme.jpg"
with open(filename, "rb") as f:
    image_msg = base64.b64encode(f.read())
endmsg = "\r\n.\r\n"

mailserver = ("smtp.gmail.com", 587)  # use for gmail

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)  # Ket noi socket voi mail server

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

# Send START TLS command
tlsCommand = 'STARTTLS\r\n'
clientSocket.send(tlsCommand.encode())
tlsRecv = clientSocket.recv(1024).decode()
print('tls receive:', tlsRecv)
if tlsRecv[:3] != '220':
    print('220 reply not received from server')

# Add SSL
clientSocket = ssl.wrap_socket(clientSocket)

# Send AUTH login command
authCommand = 'AUTH LOGIN\r\n'
clientSocket.send(authCommand.encode())
authRecv = clientSocket.recv(1024).decode()
print('After send AUTH command:', authRecv)
if authRecv[:3] != '334':  # Send AUTH accepted
    print('334 reply not received from server.')

# Send username in base 64
encodeUsername = base64.b64encode(USERNAME.encode())
stringUsername = str(encodeUsername, "utf-8") + '\r\n'
clientSocket.send(stringUsername.encode())
userRecv = clientSocket.recv(1024).decode()
print('After send username: ', userRecv)
if userRecv[:3] != '334':
    print('334 reply not received from server.')

# Send password in base 64
encodePassword = base64.b64encode(PASSWORD.encode())
stringPassword = str(encodePassword, "utf-8") + '\r\n'
clientSocket.send(stringPassword.encode())
passRecv = clientSocket.recv(1024).decode()
print('After send password: ', passRecv)
if passRecv[:3] != '235':
    print('235 reply not received from server.')

# Send MAIL FROM command and print server response.
mailFrom = 'MAIL FROM: <' + sender + '>\r\n'
clientSocket.send(mailFrom.encode())
recv2 = clientSocket.recv(1024).decode()
print('Recv2:', recv2)
if recv2[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.
rcptTo = 'RCPT TO: <' + RECIPENT + '>\r\n'
clientSocket.send(rcptTo.encode())
recv3 = clientSocket.recv(1024).decode()
print('Recv3:', recv3)
if recv3[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
recv4 = clientSocket.recv(1024).decode()
print('recv4:', recv4)
if recv4[:3] != '354':  # response to the DATA command.
    print('354 reply not received from server.')

# Send subject and msg data for message
message = 'MIME-Version: 1.0\r\n'
message += 'from:' + sender + '\r\n'
message += 'to:' + RECIPENT + '\r\n'
message += 'subject:' + subjectEmail + '\r\n'

raw = 'Content-Type: multipart/related; boundary="000000000000b6a37005bcde5e56"\r\n\r\n' \
      '--000000000000b6a37005bcde5e56\r\n' \
      'Content-Type: multipart/alternative; boundary="000000000000b6a36e05bcde5e55"\r\n\r\n' \
      '--000000000000b6a36e05bcde5e55\r\nContent-Type: text/plain; charset="UTF-8"\r\n\r\n' \
      + msg + '\r\n\r\n--000000000000b6a36e05bcde5e55\r\n' \
              'Content-Type: text/html; charset="UTF-8"\r\n\r\n' \
      + msg + '<div dir="ltr"><img src="cid:ii_klxs09zr0" alt="' \
      + filename + '" width="749" height="468"><br></div>\r\n\r\n' \
                   '--000000000000b6a36e05bcde5e55--\r\n' \
                   '--000000000000b6a37005bcde5e56\r\n'
raw += 'Content-Type: image/jpeg; name="' + filename + '"\r\n'
raw += 'Content-Disposition: attachment; filename="' + filename + '"\r\n'
raw += 'Content-Transfer-Encoding: base64\r\n'
raw += 'X-Attachment-Id: ii_klxs09zr0\r\n'
raw += 'Content-ID: <ii_klxs09zr0>\r\n\r\n'

message += raw
message = message.encode()
message += image_msg
message += '\r\n\r\n'.encode()
message += '--000000000000b6a37005bcde5e56--\r\n'.encode()
clientSocket.send(message)

# Message end with a single period.
clientSocket.send(endmsg.encode())
recv5 = clientSocket.recv(1024).decode()
print('recv5:', recv5)
if recv5[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
recv6 = clientSocket.recv(1024).decode()
print('recv6:', recv6)
if recv6[:3] != '221':  # response to the QUIT command.
    print('221 reply not received from server.')

print('send message successfully')
# close socket after send QUIT
clientSocket.close()
