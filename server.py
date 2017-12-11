import socket
import sys

class email:
     def __init__(self, mfrom, rcpts, body):
        self.mfrom = mfrom
        self.rcpts = rcpts
        self.body = body

email_list = []

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sys.stderr.write("starting on port 22222 of localhost\n")
serversock.bind(('localhost',22222))
serversock.listen(1)
while True:
    #wait for client connections
    sys.stderr.write("waiting for clients to connect\n")
    connection, client_address = serversock.accept()
    try:
        sys.stderr.write("connection established from {0} \n".format(client_address))
        message = b''
        chunk = connection.recv(16)

        if chunk.decode('utf-8') != "HELO":
            sys.stderr.write("No HELO from client\n")
            connection.sendall('ERR'.encode('utf-8'))
            break

        connection.sendall('OK'.encode('utf-8'))
        chunk = connection.recv(16)

        if chunk.decode('utf-8') != 'MFROM':
            sys.stderr.write("No MFROM from client\n")
            connection.sendall('ERR'.encode('utf-8'))
            break
        
        connection.sendall('OK'.encode('utf-8'))
        chunk = connection.recv(32)
        mfrom = chunk.decode('utf-8')
        if not ((mfrom[0] == '<') and (mfrom[-1] == '>')):
            sys.stderr.write("bad format MFROM\n")
            connection.sendall('ERR'.encode('utf-8'))
            break

        connection.sendall('OK'.encode('utf-8'))
        chunk = connection.recv(16)
        
        #Give the client their emails
        if chunk.decode('utf-8') != "get":
            sys.stderr.write("No get request from client\n")
            connection.sendall('ERR'.encode('utf-8'))
            break

        for i in range(0,len(email_list)):
            if (email_list[i].rcpts == mfrom):
                connection.sendall((email_list[i].mfrom + "\n" + email_list[i].rcpts + "\n" + email_list[i].body + "\n///").encode("utf-8"))
                chunk = connection.recv(16)
                if chunk.decode('utf-8') != "OK":
                    sys.stderr.write("No OK from client receiving inbox\n")
                    connection.sendall('ERR'.encode('utf-8'))
                    break
        
        connection.sendall('DONE'.encode('utf-8'))

        chunk = connection.recv(16)
        if chunk.decode('utf-8') != "RCPTS":
            sys.stderr.write("No RCPTS from client\n")
            connection.sendall('ERR'.encode('utf-8'))
            break

        connection.sendall('OK'.encode('utf-8'))
        chunk = connection.recv(32)


        if not(chunk.decode('utf-8').startswith('<') and chunk.decode('utf-8').endswith('>')):   #TODO: email doesnt start with < and end with >
            sys.stderr.write("bad format RCPTS\n")
            connection.sendall('ERR'.encode('utf-8'))
            break
        
        rcpts = chunk.decode('utf-8')
        print (rcpts)

        connection.sendall('OK'.encode('utf-8'))
        chunk = connection.recv(16)

        if chunk.decode('utf-8') != "BODY":
            sys.stderr.write("No BODY from client\n")
            connection.sendall('ERR'.encode('utf-8'))
            break

        connection.sendall('OK'.encode('utf-8'))
        chunk = connection.recv(1024)

        if not chunk.decode('utf-8').endswith('\n.\n'):
            sys.stderr.write("BODY text has invalid format\n")
            connection.sendall('ERR'.encode('utf-8'))
            break

        body = chunk.decode('utf-8')
        print (body)
        connection.sendall('OK'.encode('utf-8'))
        chunk = connection.recv(16)

        if chunk.decode('utf-8') != "QUIT":
            sys.stderr.write("No QUIT client. Email sent, closing connection.\n")
            connection.sendall('ERR'.encode('utf-8'))
            break

        connection.sendall('OK'.encode('utf-8'))
        newEmail = email(mfrom,rcpts,body)
        email_list.append(newEmail)
        sys.stderr.write("email received and stored. ending connection.\n")
    finally:
        connection.close()
    