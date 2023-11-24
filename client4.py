import socket
import re
import hashlib
import threading

server_ip = '127.0.0.1'
server_port = 8888

client_ip = '127.0.0.5'
client_port = 5004

chunk_size = 256 * 1024
file_path = r'C:\Users\minsoo\Downloads\file\D.file'
file_collection = []
connected_client_ip_list = []
connected_client_port_list = []


def received_broadcasting_client_data(c_socket):
    while True:
        received_client_info = c_socket.recv(1024).decode()
        print(received_client_info)
        if not received_client_info:
            break
        matches = re.findall(r'\((\d+\.\d+\.\d+\.\d+), (\d+)\)', received_client_info)
        for match in matches:
            ip_addr = match[0]
            port_num = int(match[1])
            connected_client_ip_list.append(ip_addr)
            connected_client_port_list.append(port_num)


def send_data(c_socket, f): # f -> 가지고 있는 파일
    while True:
        chunk = f.read(chunk_size)
        print(type(chunk))
        if not chunk:
            break
        c_socket.send(chunk)


def received_data(c_socket, f):
    while True:
        data = c_socket.recv(chunk_size)
        if not data:
            break
        print(f"Received data: {data}")


def calculate_file_md5(f_path):
    md5_hash = hashlib.md5()

    with open(f_path, 'rb') as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            md5_hash.update(byte_block)

    return md5_hash.hexdigest()


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    client_info = f"Client4 ({client_ip}, {client_port})"
    client_socket.send(client_info.encode())
    print(f"Client {client_socket.getsockname()[1]}: Connected to the server")

    # with open(f"Client{client_socket.getsockname()[1]}.txt", "w") as f:
    try:
        received_broadcasting_client_data(client_socket)
        print(connected_client_ip_list)
        print(connected_client_port_list)
        having_md5 = calculate_file_md5(file_path)
        client_socket.send(having_md5)
        with open(file_path, 'rb') as file:
            print()
            # send_data(client_socket, file)

    except ConnectionResetError:
        msg = f"Client {client_socket.getsockname()[1]}: Connection to the server was forcibly closed."
        print(msg)
        # f.write(msg + '\n')
    except KeyboardInterrupt:
        pass
    finally:
        msg = f"Client {client_socket.getsockname()[1]}: Connection closed"
        print(msg)
        # f.write(msg + '\n\n')
        client_socket.close()