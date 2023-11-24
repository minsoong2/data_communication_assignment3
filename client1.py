import socket
import threading

server_ip = '127.0.0.1'
port = 8888

client1_ip = '127.0.1.1'
chunk_size = 256 * 1024
file_path = r'C:\Users\minsoo\Downloads\file\A.file'

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((server_ip, port))
    print(f"Client {client_socket.getsockname()[1]}: Connected to the server")

    # with open(f"Client{client_socket.getsockname()[1]}.txt", "w") as f:
    try:
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                print(type(chunk))
                if not chunk:
                    break
                client_socket.send(chunk)

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