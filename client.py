import socket
import sys

clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 22221) #connect to where server is listening
sys.stderr.write("connecting to server at localhost port 22222\n")
clientsock.connect(server_address)

#TODO: get email data from user input
#eventually, email will be formatted properly with a header. for now just copy mfrom and rcpts to top of email.
MFROM = ("<dan@email.com>")
RCPTS = ("<john@email.com>")
MESSAGE = "Hello John,\nThis is Dan. Is your refridgerator running?\nYou better go tell it to stop running.\n.\n" #/n./n is the end of body marker


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