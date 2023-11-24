import socket
import threading

server_ip = '127.0.0.1'
server_port = 8888


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Client {client_socket.getsockname()[1]}: Connected to the server")

    with open(f"Client{client_socket.getsockname()[1]}.txt", "w") as f:
        try:
            print()
        except ConnectionResetError:
            msg = f"Client {client_socket.getsockname()[1]}: Connection to the server was forcibly closed."
            print(msg)
            f.write(msg + '\n')
        except KeyboardInterrupt:
            pass
        finally:
            msg = f"Client {client_socket.getsockname()[1]}: Connection closed"
            print(msg)
            f.write(msg + '\n\n')
            client_socket.close()