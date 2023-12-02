import socket
import re
import hashlib
import time
import threading
from _datetime import datetime

server_ip = '127.0.0.1'
server_port = 8888

client_ip = '127.0.0.2'
client_port = 5001

system_clock = 0
start_time, end_time = 0, 0

chunk_size = 256 * 1024
file_path = r'C:\Users\minsoo\Downloads\file\A.file'
file_collection = []

connected_s_client_socket_list = []
connected_r_client_socket_list = []
connected_client_ip_list = []
connected_client_port_list = []

having_md5_list = []
having_chunk_list = []


def received_broadcasting_client_data(c_socket):

    global system_clock
    current_time = time.time() * 1000
    time_difference = current_time - system_clock
    system_clock += time_difference
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
    microsecond = int((system_clock % 1000) * 1000)
    formatted_time += f".{microsecond:06d}"

    received_client_info = c_socket.recv(1024).decode()
    print(f"{formatted_time}: received_client_info -> {received_client_info}")
    matches = re.findall(r'\((\d+\.\d+\.\d+\.\d+), (\d+)\)', received_client_info)
    for match in matches:
        ip_addr = match[0]
        port_num = int(match[1])
        connected_client_ip_list.append(ip_addr)
        connected_client_port_list.append(port_num)


def calculate_file_md5(f_path):
    md5_hash = hashlib.md5()

    with open(f_path, 'rb') as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            md5_hash.update(byte_block)

    return md5_hash.hexdigest()


def connect_between_clients(c_ip, c_port):

    global system_clock
    current_time = time.time() * 1000
    time_difference = current_time - system_clock
    system_clock += time_difference
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
    microsecond = int((system_clock % 1000) * 1000)
    formatted_time += f".{microsecond:06d}"

    if c_ip != client_ip and c_port != client_port:
        time.sleep(1)
        connected_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected_socket.connect((c_ip, c_port))
        print(f"{formatted_time}: connect ->{connected_socket}")
        connected_s_client_socket_list.append(connected_socket)
    print(connected_s_client_socket_list)


def send_data(c_socket, f_path):

    global system_clock
    current_time = time.time() * 1000
    time_difference = current_time - system_clock
    system_clock += time_difference
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
    microsecond = int((system_clock % 1000) * 1000)
    formatted_time += f".{microsecond:06d}"

    with open(f_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            print(f"{formatted_time}: {chunk}")
            if chunk == b'':
                break
            c_socket.send(chunk)


def received_data(c_socket, f_path):

    global system_clock
    current_time = time.time() * 1000
    time_difference = current_time - system_clock
    system_clock += time_difference
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
    microsecond = int((system_clock % 1000) * 1000)
    formatted_time += f".{microsecond:06d}"

    c_socket.settimeout(1.0)

    with open(f_path, 'wb') as file:
        while True:
            try:
                data = c_socket.recv(chunk_size)
                if data == b'':
                    break
                file.write(data)
                print(f"{formatted_time}: received data -> {data}")
            except socket.timeout:
                break


def main():
    global system_clock, start_time, end_time

    current_time = time.time() * 1000
    time_difference = current_time - system_clock
    system_clock += time_difference
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
    microsecond = int((system_clock % 1000) * 1000)
    formatted_time += f".{microsecond:06d}"
    start_time = formatted_time

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    client_info = f"Client ({client_ip}, {client_port})"
    client_socket.send(client_info.encode())
    print(f"{formatted_time}: Client {client_socket.getsockname()[1]} Connected to the server")

    received_broadcasting_client_data(client_socket)

    md5 = calculate_file_md5(file_path)
    having_md5_list.append(md5)
    client_info_md5_data = f"Client ({client_ip}, {client_port}) {md5}"
    client_socket.send(client_info_md5_data.encode())

    received_md5_info = client_socket.recv(1024).decode()
    print(f"{formatted_time}: client_info, md5 -> {received_md5_info}")

    # with open(f"Client{client_socket.getsockname()[1]}.txt", "w") as f:
    try:

        c1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c1_socket.bind((client_ip, client_port))
        c1_socket.listen(3)

        pattern = r"\((\d+\.\d+\.\d+\.\d+), (\d+)\) \['([a-fA-F0-9]+)'\]"
        matches = re.findall(pattern, received_md5_info)
        for match in matches:
            ip_addr, port_num, md5_value = match[0], int(match[1]), match[2]
            if client_ip == ip_addr and client_port == port_num:
                continue
            elif md5_value != md5:
                connect_between_clients(ip_addr, port_num)

        for _ in range(3):
            new_client_socket, new_client_address = c1_socket.accept()
            connected_r_client_socket_list.append(new_client_socket)

        c1_send_threads, c1_receive_threads = [], []
        for cs in connected_s_client_socket_list:
            c1_s_thread = threading.Thread(target=send_data, args=(cs, file_path))
            c1_send_threads.append(c1_s_thread)

        for idx, cs in enumerate(connected_r_client_socket_list):
            save_file_path = rf'C:\Users\minsoo\Downloads\file\client1\received_new{idx + 1}.file'
            c1_r_thread = threading.Thread(target=received_data, args=(cs, save_file_path))
            c1_receive_threads.append(c1_r_thread)

        for st, rt in zip(c1_send_threads, c1_receive_threads):
            st.start()
            rt.start()

        for st, rt in zip(c1_send_threads, c1_receive_threads):
            st.join()
            rt.join()
            current_time = time.time() * 1000
            time_difference = current_time - system_clock
            system_clock += time_difference
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
            microsecond = int((system_clock % 1000) * 1000)
            formatted_time += f".{microsecond:06d}"
            end_time = formatted_time
            print(f"End time: {formatted_time}")

        client_socket.send("Transmission complete.".encode())
        print(f"{formatted_time}: Transmission complete")

        start_datetime = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
        end_datetime = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
        total_time = end_datetime - start_datetime
        print(f"Total time: {total_time}")

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


if __name__ == "__main__":
    main()