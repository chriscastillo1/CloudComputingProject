import sys
from socket import *

# Error Checking, User Must Enter Host and Filename
if len(sys.argv) != 3:
    print("ERROR - Please Enter Host followed by Directory of File")

host, file = sys.argv[1], sys.argv[2]

def connect():
    # Creates new socket to connect to server
    new_socket = socket(AF_INET, SOCK_STREAM)

    with new_socket as s:
        s.connect((host, 80))

        msg = str("GET " + file + 
            " HTTP/1.1\r\nHost: " + host + "\r\n" + 
            "Accept: text/html\r\n" + 
            "Connection: close\r\n\r\n").encode()

        s.sendall(msg)

        while True:
            response = s.recv(1024)

            if not response:
                break

            print(response.decode())

        s.shutdown(SHUT_WR)
    new_socket.close()

connect()