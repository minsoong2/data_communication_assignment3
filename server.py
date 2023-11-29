import socket
import re
import threading
import time
import random

ip = '127.0.0.1'
port = 8888
system_clock = 0
MAX_CLIENTS = 4
chunk_size = 256 * 1024
client_sockets = []
client_ips = []
client_ports = []

connected_client_list = []
c1_md5_list, c2_md5_list, c3_md5_list, c4_md5_list = [], [], [], []
c1_chunk_list, c2_chunk_list, c3_chunk_list, c4_chunk_list = [], [], [], []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ip, port))
server.listen(4)


def accept_4clients_connection():

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
            ip_addr, port_num = match.group(1), match.group(2)
            client_info = f"Client ({ip_addr}, {port_num})"
            client_ips.append(ip_addr)
            client_ports.append(port_num)
            connected_client_list.append(client_info)


def broadcast_connect_4clients(cs):
    broadcast_client_list = []
    for c_ip, c_port in zip(client_ips, client_ports):
        broadcast_msg = f"Client ({c_ip}, {c_port})"
        broadcast_client_list.append(broadcast_msg)
    print(broadcast_client_list)
    send_msg = ' '.join(broadcast_client_list)
    cs.send(send_msg.encode())


def receive_and_store_md5_data(cs):
    client_info_md5_data = cs.recv(1024).decode()
    print(client_info_md5_data)
    match = re.search(r'\((\d+\.\d+\.\d+\.\d+), (\d+)\) \b([a-fA-F0-9]{32})\b', client_info_md5_data)
    ip_addr, port_num = match.group(1), match.group(2)
    client_info = f"Client ({ip_addr}, {port_num})"
    c_md5 = match.group(3)
    if client_info == connected_client_list[0]:
        c1_md5_list.append(c_md5)
    elif client_info == connected_client_list[1]:
        c2_md5_list.append(c_md5)
    elif client_info == connected_client_list[2]:
        c3_md5_list.append(c_md5)
    elif client_info == connected_client_list[3]:
        c4_md5_list.append(c_md5)


def broadcast_md5_info(cs):
    msg = f"Client ({client_ips[0]}, {client_ports[0]}) {c1_md5_list} " \
          f"Client ({client_ips[1]}, {client_ports[1]}) {c2_md5_list} " \
          f"Client ({client_ips[2]}, {client_ports[2]}) {c3_md5_list} " \
          f"Client ({client_ips[3]}, {client_ports[3]}) {c4_md5_list}"
    cs.send(msg.encode())


def main():
    accept_4clients_connection()

    broadcast_connect_info_threads = []
    for cs in client_sockets:
        server_thread = threading.Thread(target=broadcast_connect_4clients, args=(cs,))
        server_thread.start()
        broadcast_connect_info_threads.append(server_thread)

    for t in broadcast_connect_info_threads:
        t.join()

    receive_md5_threads = []
    for cs in client_sockets:
        server_thread = threading.Thread(target=receive_and_store_md5_data, args=(cs,))
        server_thread.start()
        receive_md5_threads.append(server_thread)

    for t in receive_md5_threads:
        t.join()

    broadcast_md5_info_threads = []
    for cs in client_sockets:
        server_thread = threading.Thread(target=broadcast_md5_info, args=(cs,))
        server_thread.start()
        broadcast_md5_info_threads.append(server_thread)

    for t in broadcast_md5_info_threads:
        t.join()


if __name__ == "__main__":
    main()