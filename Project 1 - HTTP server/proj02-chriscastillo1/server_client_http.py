import sys
import traceback
import os.path
from os import path
from socket import *
from threading import *

def main():
    if len(sys.argv) != 2:
        print("ERROR - Please Enter Port")
    else:
        port = int(sys.argv[1])
    # Starting up server
    print("Starting up Local Server\n")
    construct_server(port)

def construct_server(port):
    # Creates Server Socket
    listen_socket = create_socket(port)
    print("Creating Server Socket")

    # Opens Socket For Listening
    listen_socket.listen(5)
    print("Socket is Now Listening")

    while True:
        con, addr = listen_socket.accept()
        print(f"Connected to: {addr[0]} on Port: {addr[1]}\n")

        try:
            thread_client = Thread(target=thread_process, args=(con,)).start()
        except:
            print("THREAD HANDLER DID NOT START\r\n")
            traceback.print_exc()

    listen_socket.close()

def thread_process(conn_socket):
    # Opens incoming client request
    incoming_data = conn_socket.recv(1024)
    file = incoming_data.split()[1]
    print("File Request: " + str(file))
    # Checks if file exists, if so it then opens and sends back file contents
    if (path.isfile(file)):
        
        content = os.stat(file).st_size

        header = str("HTTP/1.1 200 OK\nContent-Length: " + 
                str(content) + "\n" + "Content-Type: text/html\r\n")

        conn_socket.sendall(header.encode())

        f = open(file, 'rb')
        l = f.read(1024)
        while (l):
            conn_socket.send(l)
            l = f.read(1024)
        f.close()
    else:

        header = "HTTP/1.1 404 Not Found\r\n"
        conn_socket.sendall(header.encode())

    conn_socket.close()

def create_socket(port):
    listen_socket = socket(AF_INET, SOCK_STREAM)

    # Creates sever address / localhost on port 8080
    host, port = "localhost", port

    # Binds server address to listening socket
    listen_socket.bind((host, port))
    return listen_socket

if __name__ == "__main__":
    main()