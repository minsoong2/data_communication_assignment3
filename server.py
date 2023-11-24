import socket
import re
import threading
import random
import time

ip = '127.0.0.1'
port = 8888
system_clock = 0
MAX_CLIENTS = 4
chunk_size = 256 * 1024
client_sockets = []
client_ips = []
client_ports = []
broadcast_msg_list = []


def accept_4clients_connection():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen(1)
    client_accept_cnt = 0

    if client_accept_cnt == 0:
        listen = "Server is listening..."
        print(listen)
        # f.write(listen + '\n')

    while client_accept_cnt < MAX_CLIENTS:
        client_socket, client_address = server.accept()
        accept = f"Accepted connection from {client_address}"
        print(accept)
        # f.write(accept + '\n')
        client_sockets.append(client_socket)
        client_accept_cnt += 1
        received_client_info = client_socket.recv(1024).decode()
        match = re.search(r'\((\d+\.\d+\.\d+\.\d+), (\d+)\)', received_client_info)
        if match:
            ip_addr = match.group(1)
            port_num = match.group(2)
            client_ips.append(ip_addr)
            client_ports.append(port_num)


def broadcast_4clients():
    for c_ip, c_port in zip(client_ips, client_ports):
        broadcast_msg = f"Client ({c_ip}, {c_port})"
        broadcast_msg_list.append(broadcast_msg)
    print(broadcast_msg_list)
    send_msg = ' '.join(broadcast_msg_list)
    for cs in client_sockets:
        cs.send(send_msg.encode())


def main():
    accept_4clients_connection()
    broadcast_4clients()


if __name__ == "__main__":
    main()