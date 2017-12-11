import socket
import sys

clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 22222) #connect to where server is listening
sys.stderr.write("connecting to server at localhost port 22222\n")
clientsock.connect(server_address)


MFROM = input("Please enter your email address.")
MFROM = "<" + MFROM + ">"

clientsock.sendall('HELO'.encode('utf-8'))
chunk = clientsock.recv(16)
if chunk.decode('utf-8') != "OK":
    sys.stderr.write("No OK to HELO\n")
    clientsock.close


clientsock.sendall('MFROM'.encode('utf-8'))
chunk = clientsock.recv(16)
if chunk.decode('utf-8') != "OK":
    sys.stderr.write("No OK to MFROM\n")
    clientsock.close


clientsock.sendall(MFROM.encode('utf-8'))
chunk = clientsock.recv(16)
if chunk.decode('utf-8') != "OK":
    sys.stderr.write("No OK to MFROM email\n")
    clientsock.close

clientsock.sendall("get".encode('utf-8'))
print("Hello, " + MFROM + ". Here are your emails:\n")
while 1:
    chunk = clientsock.recv(1096)
    if(chunk.decode('utf-8') != "DONE"):
        print(chunk.decode("utf-8"))
        print("END OF EMAIL\n")
        clientsock.sendall("OK".encode('utf-8'))
    else:
        break
print("INBOX HAS BEEN READ.\n")

#get emails


RCPTS = input("Please enter the recipients email address.")
RCPTS = "<" + RCPTS + ">"
MESSAGE = input("Please enter the body of your email address.")
MESSAGE = MESSAGE + "\n.\n" #/n./n is the end of body marker

clientsock.sendall('RCPTS'.encode('utf-8'))
chunk = clientsock.recv(16)
if chunk.decode('utf-8') != "OK":
    sys.stderr.write("No OK to RCPTS\n")
    clientsock.close


clientsock.sendall(RCPTS.encode('utf-8'))
chunk = clientsock.recv(16)
if chunk.decode('utf-8') != "OK":
    sys.stderr.write("No OK to RCPTS email\n")
    clientsock.close


clientsock.sendall('BODY'.encode('utf-8'))
chunk = clientsock.recv(16)
if chunk.decode('utf-8') != "OK":
    sys.stderr.write("No OK to BODY\n")
    clientsock.close


clientsock.sendall(MESSAGE.encode('utf-8'))
chunk = clientsock.recv(16)
if chunk.decode('utf-8') != "OK":
    sys.stderr.write("No OK to MESSAGE\n")
    clientsock.close


sys.stderr.write("Email sent sucessfully\n")
clientsock.sendall('QUIT'.encode('utf-8'))
chunk = clientsock.recv(16)
if chunk.decode('utf-8') != "OK":
    sys.stderr.write("No OK to QUIT\n")
    clientsock.close


sys.stderr.write("Session Closed\n")
clientsock.close()