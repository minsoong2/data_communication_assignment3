import socket
import threading
import random
import time

ip = '127.0.0.1'
port = 8888
system_clock = 0
MAX_CLIENTS = 4
chunk_size = 256 * 1024
client_sockets = []


def accept_4clients_connection():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen(1)

    # client_accept_cnt = 0

    # if client_accept_cnt == 0:
    listen = "Server is listening..."
    print(listen)
    # f.write(listen + '\n')

    # while client_accept_cnt < MAX_CLIENTS:
    client_socket, client_address = server.accept()
    accept = f"Accepted connection from {client_address}"
    print(accept)
    # f.write(accept + '\n')
    client_sockets.append(client_socket)
    # client_accept_cnt += 1

    while True:
        data = client_socket.recv(chunk_size)
        if not data:
            break
        print(data)

    client_socket.close()


def main():
    accept_4clients_connection()


if __name__ == "__main__":
    main()