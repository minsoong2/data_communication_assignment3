import socket
import re
import hashlib
import time
import threading

server_ip = '127.0.0.1'
server_port = 8888

client_ip = '127.0.0.5'
client_port = 5004

chunk_size = 256 * 1024
file_path = r'C:\Users\minsoo\Downloads\file\D.file'
file_collection = []
connected_s_client_socket_list = []
connected_r_client_socket_list = []
connected_client_ip_list = []
connected_client_port_list = []
having_md5_list = []
having_chunk_list = []


def calculate_file_md5(f_path):
    md5_hash = hashlib.md5()

    with open(f_path, 'rb') as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            md5_hash.update(byte_block)

    return md5_hash.hexdigest()


def received_broadcasting_client_data(c_socket):
    received_client_info = c_socket.recv(1024).decode()
    print(received_client_info)
    matches = re.findall(r'\((\d+\.\d+\.\d+\.\d+), (\d+)\)', received_client_info)
    for match in matches:
        ip_addr = match[0]
        port_num = int(match[1])
        connected_client_ip_list.append(ip_addr)
        connected_client_port_list.append(port_num)


def send_data(c_socket, f_path):
    with open(f_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            print(type(chunk))
            if not chunk:
                break
            c_socket.send(chunk)


def received_data(c_socket):
    while True:
        data = c_socket.recv(chunk_size)
        if not data:
            break
        print(type(data))


def connect_between_clients(c_ip, c_port):
    if c_ip != client_ip and c_port != client_port:
        time.sleep(1)
        connected_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected_socket.connect((c_ip, c_port))
        print(connected_socket)
        connected_s_client_socket_list.append(connected_socket)
    print(connected_s_client_socket_list)


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    client_info = f"Client4 ({client_ip}, {client_port})"
    client_socket.send(client_info.encode())
    print(f"Client {client_socket.getsockname()[1]}: Connected to the server")

    received_broadcasting_client_data(client_socket)
    print(connected_client_ip_list, connected_client_port_list)

    md5 = calculate_file_md5(file_path)
    having_md5_list.append(md5)
    client_info_md5_data = f"Client ({client_ip}, {client_port}) {md5}"
    client_socket.send(client_info_md5_data.encode())

    received_md5_info = client_socket.recv(1024).decode()
    print(received_md5_info)

    # with open(f"Client{client_socket.getsockname()[1]}.txt", "w") as f:
    try:

        c4_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c4_socket.bind((client_ip, client_port))
        c4_socket.listen(3)

        pattern = r"\((\d+\.\d+\.\d+\.\d+), (\d+)\) \['([a-fA-F0-9]+)'\]"
        matches = re.findall(pattern, received_md5_info)
        for match in matches:
            ip_addr, port_num, md5_value = match[0], int(match[1]), match[2]
            if client_ip == ip_addr and client_port == port_num:
                continue
            elif md5_value != md5:
                connect_between_clients(ip_addr, port_num)

        for _ in range(3):
            new_client_socket, new_client_address = c4_socket.accept()
            connected_r_client_socket_list.append(new_client_socket)
            # f.write(accept + '\n')

    except ConnectionResetError:
        msg = f"Client {client_socket.getsockname()[1]}: Connection was forcibly closed."
        print(msg)
        # f.write(msg + '\n')
    except KeyboardInterrupt:
        pass
    finally:
        msg = f"Client {client_socket.getsockname()[1]}: Connection closed"
        print(msg)
        # f.write(msg + '\n\n')
        client_socket.close()