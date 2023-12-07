import socket
import re
import threading
import time
from _datetime import datetime

ip = 'ec2-3-38-191-66.ap-northeast-2.compute.amazonaws.com'
port = 8888

system_clock = 0
start_time, end_time = 0, 0

MAX_CLIENTS = 4
chunk_size = 256 * 1024
client_sockets = []
client_ips = []
client_ports = []
connected_client_list = []

c1_md5_list, c2_md5_list, c3_md5_list, c4_md5_list = [], [], [], []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ip, port))
server.listen(4)


def accept_4clients_connection(f):
    global system_clock, start_time
    client_accept_cnt = 0
    current_time = time.time() * 1000
    time_difference = current_time - system_clock
    system_clock += time_difference
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
    microsecond = int((system_clock % 1000) * 1000)
    formatted_time += f".{microsecond:06d}"

    if client_accept_cnt == 0:
        start_time = formatted_time
        print(f"Start time: {formatted_time}")
        f.write(f"Start time: {formatted_time}" + '\n')
        listen = "Server is listening..."
        print(f"{formatted_time}: {listen}")
        f.write(f"{formatted_time}: {listen}" + '\n')

    while client_accept_cnt < MAX_CLIENTS:

        client_socket, client_address = server.accept()
        accept = f"Accepted connection from {client_address}"

        current_time = time.time() * 1000
        time_difference = current_time - system_clock
        system_clock += time_difference
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
        microsecond = int((system_clock % 1000) * 1000)
        formatted_time += f".{microsecond:06d}"
        print(f"{formatted_time}: {accept}")
        f.write(f"{formatted_time}: {accept}" + '\n')

        client_sockets.append(client_socket)
        client_accept_cnt += 1
        received_client_info = client_socket.recv(1024).decode()
        match = re.findall(r'\(([^,]+), (\d+)\)', received_client_info)
        print(match)
        if match:
            ip_addr, port_num = match[0][0], match[0][1]
            client_info = f"Client ({ip_addr}, {port_num})"
            client_ips.append(ip_addr)
            client_ports.append(port_num)
            connected_client_list.append(client_info)


def broadcast_connect_4clients(cs, f):
    global system_clock
    broadcast_client_list = []

    for c_ip, c_port in zip(client_ips, client_ports):
        broadcast_msg = f"Client ({c_ip}, {c_port})"
        broadcast_client_list.append(broadcast_msg)
    send_msg = ' '.join(broadcast_client_list)
    cs.send(send_msg.encode())

    current_time = time.time() * 1000
    time_difference = current_time - system_clock
    system_clock += time_difference
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
    microsecond = int((system_clock % 1000) * 1000)
    formatted_time += f".{microsecond:06d}"
    print(f"{formatted_time}: Send client list to {cs}")
    f.write(f"{formatted_time}: Send client list to {cs}" + '\n')


def receive_and_store_md5_data(cs, f):
    global system_clock
    client_info_md5_data = cs.recv(1024).decode()
    match = re.search(r'\((\d+\.\d+\.\d+\.\d+), (\d+)\) \b([a-fA-F0-9]{32})\b', client_info_md5_data)
    ip_addr, port_num = match.group(1), match.group(2)
    client_info = f"Client ({ip_addr}, {port_num})"
    c_md5 = match.group(3)

    current_time = time.time() * 1000
    time_difference = current_time - system_clock
    system_clock += time_difference
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
    microsecond = int((system_clock % 1000) * 1000)
    formatted_time += f".{microsecond:06d}"
    print(f"{formatted_time}: Received client info {client_info}: {c_md5}")
    f.write(f"{formatted_time}: Received client info {client_info}: {c_md5}" + '\n')

    if client_info == connected_client_list[0]:
        c1_md5_list.append(c_md5)
    elif client_info == connected_client_list[1]:
        c2_md5_list.append(c_md5)
    elif client_info == connected_client_list[2]:
        c3_md5_list.append(c_md5)
    elif client_info == connected_client_list[3]:
        c4_md5_list.append(c_md5)


def broadcast_md5_info(cs, f):
    global system_clock
    current_time = time.time() * 1000
    time_difference = current_time - system_clock
    system_clock += time_difference
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
    microsecond = int((system_clock % 1000) * 1000)
    formatted_time += f".{microsecond:06d}"

    msg = f"Client ({client_ips[0]}, {client_ports[0]}) {c1_md5_list} " \
          f"Client ({client_ips[1]}, {client_ports[1]}) {c2_md5_list} " \
          f"Client ({client_ips[2]}, {client_ports[2]}) {c3_md5_list} " \
          f"Client ({client_ips[3]}, {client_ports[3]}) {c4_md5_list}"

    f.write(f"{formatted_time}: Send client info -> {msg}" + '\n')
    cs.send(msg.encode())


def receive_chunk_info(cs, f):
    global system_clock
    current_time = time.time() * 1000
    time_difference = current_time - system_clock
    system_clock += time_difference
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
    microsecond = int((system_clock % 1000) * 1000)
    formatted_time += f".{microsecond:06d}"

    while True:
        chunk_len_data = cs.recv(1024).decode()
        if not chunk_len_data:
            break
        f.write(chunk_len_data + '\n')


def receive_complete_info(cs, f):
    global system_clock
    current_time = time.time() * 1000
    time_difference = current_time - system_clock
    system_clock += time_difference
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
    microsecond = int((system_clock % 1000) * 1000)
    formatted_time += f".{microsecond:06d}"

    complete_msg = cs.recv(1024).decode()
    print(complete_msg)
    f.write(complete_msg + '\n')


def main():
    global system_clock, start_time, end_time

    with open('server.txt', 'w', encoding='utf-8') as server_f:
        current_time = time.time() * 1000
        time_difference = current_time - system_clock
        system_clock += time_difference
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
        microsecond = int((system_clock % 1000) * 1000)
        formatted_time += f".{microsecond:06d}"

        accept_4clients_connection(server_f)

        broadcast_connect_info_threads = []
        for cs in client_sockets:
            server_thread = threading.Thread(target=broadcast_connect_4clients, args=(cs, server_f))
            server_thread.start()
            broadcast_connect_info_threads.append(server_thread)

        for t in broadcast_connect_info_threads:
            t.join()

        receive_md5_threads = []
        for cs in client_sockets:
            server_thread = threading.Thread(target=receive_and_store_md5_data, args=(cs, server_f))
            server_thread.start()
            receive_md5_threads.append(server_thread)

        for t in receive_md5_threads:
            t.join()

        broadcast_md5_info_threads = []
        for cs in client_sockets:
            server_thread = threading.Thread(target=broadcast_md5_info, args=(cs, server_f))
            server_thread.start()
            broadcast_md5_info_threads.append(server_thread)

        for t in broadcast_md5_info_threads:
            t.join()

        chunk_info_threads = []
        for cs in client_sockets:
            server_thread = threading.Thread(target=receive_chunk_info, args=(cs, server_f))
            server_thread.start()
            chunk_info_threads.append(server_thread)

        for t in chunk_info_threads:
            t.join()

        msg_r_threads = []
        for cs in client_sockets:
            server_thread = threading.Thread(target=receive_complete_info, args=(cs, server_f))
            server_thread.start()
            msg_r_threads.append(server_thread)

        for t in msg_r_threads:
            t.join()

        for cs in client_sockets:
            client_md_info = cs.recv(1024).decode()
            print(client_md_info)
            server_f.write(client_md_info + '\n')

        current_time = time.time() * 1000
        time_difference = current_time - system_clock
        system_clock += time_difference
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
        microsecond = int((system_clock % 1000) * 1000)
        formatted_time += f".{microsecond:06d}"
        end_time = formatted_time

        print(f"End time: {formatted_time}")
        server_f.write(f"End time: {formatted_time}" + '\n')

        start_datetime = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
        end_datetime = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
        total_time = end_datetime - start_datetime
        print(f"Total time: {total_time}")
        server_f.write(f"Total time: {total_time}" + '\n')

        for cs in client_sockets:
            cs.close()

        server.close()
        print("server closed...")
        server_f.write("server closed..." + '\n')


if __name__ == "__main__":
    main()
