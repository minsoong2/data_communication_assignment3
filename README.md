# 💡 Data Communications Programming Assignment - Fall 2023

## 🌟P2P File-Sharing System Implementation

### 📘Project Overview

This assignment involves the implementation of a P2P (Peer-to-Peer) file-sharing system using a server and multiple client architecture. The system utilizes multi-threading and socket communication for efficient data transfer.

### 📘Due Date

- Submission Deadline: December 7, 2023, 23:59
- No late submissions will be accepted.

### 📘Simulation Environment and Components

- **Server**: Maintains a System Clock, manages client connections, and coordinates file chunk distribution.
- **Clients**: Four clients, each initially holding a unique 500MB file divided into 256KB chunks.
- **Chunk Distribution**: Clients request and receive file chunks from each other, aiming to gather all chunks of every file.
- **System Clock**: Used to measure the total time taken for file distribution.

### 📘Server.py Components

**Functions:**
- `accept_4clients_connection()`: Manages the connection of 4 clients per server thread.
- `broadcast_connect_4clients()`: Sends the connected clients' information (IP and port) to all clients.
- `receive_and_store_md5_data()`: Receives and stores MD5 data from each client.
- `broadcast_md5_info()`: Sends all connected clients' IP, port, and MD5 information to each client.
- `receive_chunk_info()`: Receives chunk information from clients.
- `receive_complete_info()`: Receives complete information from clients.
- `main()`: Executes the main routine, managing client connections, data transmission, and information dissemination.

**Global Variables:**
- `system_clock`: Stores the system time incremented for each operation.
- `start_time`, `end_time`: Stores the start and end times of the program.
- `MAX_CLIENTS`: Indicates the maximum number of clients to connect.
- `chunk_size`: Size of the data chunk used in file transmission.
- `client_sockets`: List to manage client socket connections.
- `client_ips`, `client_ports`: Lists storing IP addresses and port numbers of each client.
- `connected_client_list`: List storing the information of connected clients.
- `c1_md5_list`, `c2_md5_list`, `c3_md5_list`, `c4_md5_list`: Lists storing MD5 hash values for each client.
- `server`: Variable representing the server socket.

**Variables:**
- `client_accept_cnt`: Tracks the number of client connections.
- `current_time`: Stores the current time in milliseconds.
- `time_difference`, `formatted_time`, `microsecond`: Variables for time calculations and formatting.
- `listen`, `accept`: Variables for server listen and accept messages.
- `start_time`: Stores the start time of the server.
- `broadcast_client_list`, `send_msg`: Variables for storing client list and message for broadcasting.
- `client_info_md5_data`: Stores MD5 data received from clients.
- `ip_addr`, `port_num`, `client_info`, `c_md5`: Variables for storing client information and MD5 checksums.

### 📘Client.py Components

**Functions:**
- `received_broadcasting_client_data(c_socket, f)`: Receives broadcasting data from the server.
- `calculate_file_md5(f_path)`: Calculates the MD5 hash of a file.
- `connect_between_clients(c_ip, c_port, f)`: Establishes a connection between clients.
- `send_data(c_socket, f_path, f)`: Sends file data to another client.
- `received_data(c_socket, f_path, f)`: Receives data from another client.
- `calculate_md5_for_files_in_directory(directory)`: Calculates MD5 values for files in a directory.
- `main()`: Executes the main routine of the client.

**Global Variables:**
- `server_ip`, `server_port`, `client_ip`, `client_port`, `system_clock`, `start_time`, `end_time`, `chunk_size`, `file_path`, `file_collection`.
- `connected_client_ip_list`, `connected_client_port_list`, `having_md5_list`, `having_chunk_list1`, `having_chunk_list2`, `having_chunk_list3`.
- `client_socket`.

**Variables:**
- `current_time`, `time_difference`, `formatted_time`, `received_client_info`, `file`, `chunk`, `data`.
- `md5_dict`, `md5`, `client_info`, `client_info_md5_data`, `received_md5_info`.
- `c1_socket`, `matches`, `ip_addr`, `port_num`, `md5_value`.
- `new_client_socket`, `new_client_address`, `c1_send_threads`, `c1_receive_threads`, `st`, `rt`.
- `download_file_path`, `md5_results`, `file_name`.

### 📘Compilation Method

No compilation is required as the source code is written in Python. Python version 3.9 or higher and an appropriate IDE are necessary.

### 📘Program Execution Environment and Method

**Environment:**
- Python version 3.9 & Pycharm community edition version 2023.2.3.
- AWS EC2 instance (Ubuntu).

**Execution Method:**
- On the EC2 instance, execute `server.py`, `client1.py`, and `client2.py`.
- Locally, run `client3.py` and `client4.py` using PyCharm.

### 📘Optimized Algorithm Implementation

#### Step 1: 서버가 클라이언트와 연결하면서 클라이언트의 IP와 포트 정보를 수집
server.connect4Clients()

#### Step 2: 서버는 클라이언트의 IP와 포트 정보를 묶어서 다시 클라이언트에게 송신
connectedClientsInfo = server.getConnectedClientsInfo()
server.sendTo4Clients(connectedClientsInfo)

#### Step 3: 클라이언트는 자신의 .file의 MD5 값을 서버에 송신
client.sendFileMD5ToServer()

#### Step 4: 서버는 클라이언트 정보(ip,port)와 파일 MD5 값을 모든 클라이언트에 뿌려줌
allClientsInfo = server.getAllClientsInfoWithFileMD5()
server.sendTo4Clients(allClientsInfo)

#### Step 5: 클라이언트는 자신이 가지고 있지 않은 MD5 값을 가진 클라이언트에게 파일을 요청하고, 자신이 가지고 있는 MD5 값을 상대 클라이언트에게 송신
for eachClientInfo in allClientsInfo:  
    if client.hasFileMD5(eachClientInfo.fileMD5) is False:  
        client.requestFileFromOtherClient(eachClientInfo.ip, eachClientInfo.port)  
    if client.hasFileMD5(eachClientInfo.fileMD5) and \  
            eachClientInfo.ip != client.getOwnIP() and \  
            eachClientInfo.port != client.getOwnPort():  
        client.sendOwnFileMD5ToOtherClient(eachClientInfo.ip, eachClientInfo.port)  

- The server connects with clients, gathering their IP and port information, and broadcasts this information to all clients.
- Clients calculate the MD5 hash of their files and send it to the server.
- The server then broadcasts each client's IP, port, and MD5 information.
- Clients request files from others based on MD5 values and send their files to clients that need them.

### 📘Error or Additional Message Handling

- ConnectionResetError: Outputs "Client 1: Connection was forcibly closed." and terminates the program.
- KeyboardInterrupt: Outputs "Client 1: Connection closed" and terminates the program.

### 🚀Simulation Scenario

- The server starts with a System Clock at 0.0 msec.
- Clients connect to the server, exchange file chunk information, and request necessary chunks from each other.
- The server does not hold actual files but facilitates the distribution of chunks between clients.
- Each client logs all events and operations, including the download time for each file chunk and the completion of the entire file.

### 🚀Submission Details

- Submit a zip file named `G<group_number>HW3.zip` containing all source files and log files.
- Include a `Readme.txt` detailing the group name, members, roles, program components, compilation method, execution environment, and method.
- Provide the pseudo-code and explanation of the implemented algorithm for optimizing file transfers.
- Describe how errors and additional messages were handled.

### 🚀Video Explanation

- Create a 5-minute explanatory video and provide a download link in a `download.txt` file.
- Ensure the video is accessible for evaluation; any issues with the video will result in penalties.

### 🚀Additional Comments

- The server must be physically hosted externally (e.g., on AWS or Google Cloud).
- All communication between the server and clients must be implemented using sockets.
- The system should be designed to minimize the total time for file transfers.
- Each client's file transfer time should be measured from the moment of server connection to the completion of all file downloads.

For more detailed information, refer to the `HW3description.pdf` document provided with the assignment.
