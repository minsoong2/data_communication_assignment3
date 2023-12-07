import socket
import re
import hashlib
import time
import threading
import os
from _datetime import datetime

server_ip = 'ec2-3-38-191-66.ap-northeast-2.compute.amazonaws.com'
server_port = 8888

client_ip = '59.22.140.243'
client_port = 5004

system_clock = 0
start_time, end_time = 0, 0

chunk_size = 256 * 1024
file_path = r'C:\Users\lbg48\Downloads\file\client4\D.file'
file_collection = []

connected_s_client_socket_list = []
connected_r_client_socket_list = []
connected_client_ip_list = []
connected_client_port_list = []

having_md5_list = []
having_chunk_list1 = []
having_chunk_list2 = []
having_chunk_list3 = []

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))
c4_send_threads, c4_receive_threads = [], []


def received_broadcasting_client_data(c_socket, f):

    global system_clock
    current_time = time.time() * 1000
    time_difference = current_time - system_clock
    system_clock += time_difference
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
    microsecond = int((system_clock % 1000) * 1000)
    formatted_time += f".{microsecond:06d}"

    received_client_info = c_socket.recv(1024).decode()
    print(f"{formatted_time}: received_client_info -> {received_client_info}")
    f.write(f"{formatted_time}: received_client_info -> {received_client_info}" + '\n')
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


def connect_between_clients(c_ip, c_port, f):

    global system_clock
    current_time = time.time() * 1000
    time_difference = current_time - system_clock
    system_clock += time_difference
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
    microsecond = int((system_clock % 1000) * 1000)
    formatted_time += f".{microsecond:06d}"

    if c_port != client_port:
        time.sleep(1)
        connected_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected_socket.connect((c_ip, c_port))
        print(f"{formatted_time}: connect -> {connected_socket}")
        connected_s_client_socket_list.append(connected_socket)
        f.write(f"{formatted_time}: connect -> {connected_socket}" + '\n')
        c4_s_thread = threading.Thread(target=send_data, args=(connected_socket, file_path, f))
        c4_s_thread.start()
        c4_send_threads.append(c4_s_thread)
    print(connected_s_client_socket_list)


def send_data(c_socket, f_path, f):

    global system_clock
    cnt = 0

    with open(f_path, 'rb') as file:
        while True:
            current_time = time.time() * 1000
            time_difference = current_time - system_clock
            system_clock += time_difference
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
            microsecond = int((system_clock % 1000) * 1000)
            formatted_time += f".{microsecond:06d}"

            time.sleep(0.3)
            cnt += 1
            chunk = file.read(chunk_size)
            print(f"{formatted_time}: {cnt}client4 sends chunk")
            f.write(f"{formatted_time}: client4 sends chunk" + '\n')
            if chunk == b'':
                break
            c_socket.send(chunk)


def received_data(c_socket, f_path, f):

    global system_clock
    c_socket.settimeout(1.0)

    with open(f_path, 'wb') as file:
        while True:

            current_time = time.time() * 1000
            time_difference = current_time - system_clock
            system_clock += time_difference
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
            microsecond = int((system_clock % 1000) * 1000)
            formatted_time += f".{microsecond:06d}"

            try:
                time.sleep(0.3)
                data = c_socket.recv(chunk_size)
                if data == b'':
                    break
                file.write(data)

                if "received_new1" in f_path:
                    having_chunk_list1.append(data)
                elif "received_new2" in f_path:
                    having_chunk_list2.append(data)
                elif "received_new3" in f_path:
                    having_chunk_list3.append(data)

                chunk_list1_len, chunk_list2_len, chunk_list3_len = len(having_chunk_list1), len(having_chunk_list2), len(having_chunk_list3)
                chunk_list_len = f"{formatted_time}: client4 md5 - {having_md5_list[0]}, chunk_list1_len: {chunk_list1_len}, chunk_list2_len: {chunk_list2_len}, chunk_list3_len: {chunk_list3_len}"
                client_socket.send(chunk_list_len.encode())
                f.write(chunk_list_len + '\n')

                f.write(f"{formatted_time}: received data" + '\n')
            except socket.timeout:
                break


def calculate_md5_for_files_in_directory(directory):
    md5_dict = {}
    for file_name in os.listdir(directory):
        if file_name.endswith(".file"):
            f_path = os.path.join(directory, file_name)
            md5_value = calculate_file_md5(f_path)
            md5_dict[file_name] = md5_value
    return md5_dict


def main():
    with open("client4.txt", "w", encoding='utf-8') as client_f:
        global system_clock, start_time, end_time

        current_time = time.time() * 1000
        time_difference = current_time - system_clock
        system_clock += time_difference
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
        microsecond = int((system_clock % 1000) * 1000)
        formatted_time += f".{microsecond:06d}"
        start_time = formatted_time

        client_info = f"Client ({client_ip}, {client_port})"
        client_socket.send(client_info.encode())
        print(f"{formatted_time}: Client 4 Connected to the server")
        client_f.write(f"{formatted_time}: Client 4 Connected to the server" + '\n')

        received_broadcasting_client_data(client_socket, client_f)

        md5 = calculate_file_md5(file_path)
        having_md5_list.append(md5)
        client_info_md5_data = f"Client ({client_ip}, {client_port}) {md5}"

        current_time = time.time() * 1000
        time_difference = current_time - system_clock
        system_clock += time_difference
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
        microsecond = int((system_clock % 1000) * 1000)
        formatted_time += f".{microsecond:06d}"
        print(f"{formatted_time}: client_info, md5 -> server {client_info_md5_data}" + '\n')
        client_socket.send(client_info_md5_data.encode())
        client_f.write(f"{formatted_time}: client_info, md5 -> server {client_info_md5_data}" + '\n')

        current_time = time.time() * 1000
        time_difference = current_time - system_clock
        system_clock += time_difference
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(system_clock / 1000))
        microsecond = int((system_clock % 1000) * 1000)
        formatted_time += f".{microsecond:06d}"
        received_md5_info = client_socket.recv(1024).decode()
        print(f"{formatted_time}: client_info, md5 -> {received_md5_info}")
        client_f.write(f"{formatted_time}: client_info, md5 -> {received_md5_info}" + '\n')

        try:

            c4_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c4_socket.bind(('0.0.0.0', client_port))
            c4_socket.listen(3)

            pattern = r"\((\d+\.\d+\.\d+\.\d+), (\d+)\) \['([a-fA-F0-9]+)'\]"
            matches = re.findall(pattern, received_md5_info)
            for idx, match in enumerate(matches):
                ip_addr, port_num, md5_value = match[0], int(match[1]), match[2]
                if client_ip == ip_addr and client_port == port_num:
                    continue
                elif md5_value != md5:
                    connect_between_clients(ip_addr, port_num, client_f)
                new_client_socket, new_client_address = c4_socket.accept()
                save_file_path = rf'C:\Users\lbg48\Downloads\file\client4\received_new{idx + 1}.file'
                c4_r_thread = threading.Thread(target=received_data, args=(new_client_socket, save_file_path, client_f))
                c4_r_thread.start()
                c4_receive_threads.append(c4_r_thread)

            for st, rt in zip(c4_send_threads, c4_receive_threads):
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
            client_f.write(f"End time: {formatted_time}" + '\n')

            print(f"{formatted_time}: Transmission complete")
            client_socket.send(f"{formatted_time}: Transmission complete".encode())
            client_f.write(f"{formatted_time}: Transmission complete" + '\n')

            start_datetime = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            end_datetime = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
            total_time = end_datetime - start_datetime
            print(f"Total time: {total_time}")
            client_f.write(f"Total time: {total_time}" + '\n')

            download_file_path = r'C:\Users\lbg48\Downloads\file\client4'
            md5_results = calculate_md5_for_files_in_directory(download_file_path)
            for file_name, md5_value in md5_results.items():
                print(f"{file_name}: {md5_value}")
                if md5_value not in having_md5_list:
                    having_md5_list.append(md5_value)

            having_md5_info = f"{formatted_time}: client4 md5 - {having_md5_list[0]}, {having_md5_list[1]}, {having_md5_list[2]}, {having_md5_list[3]}"
            print(having_md5_info)
            client_f.write(having_md5_info + '\n')
            client_socket.send(having_md5_info.encode())

        except ConnectionResetError:
            msg = f"Client {client_socket.getsockname()[1]}: Connection was forcibly closed."
            print(msg)
        except KeyboardInterrupt:
            pass
        finally:
            msg = f"Client {client_socket.getsockname()[1]}: Connection closed"
            print(msg)
            for cs in connected_s_client_socket_list:
                cs.close()
            for cs in connected_r_client_socket_list:
                cs.close()
            c4_socket.close()
            client_socket.close()


if __name__ == "__main__":
    main()