# 💡 Data Communications Programming Assignment - Fall 2022

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
- `accept_4clients_connection()`: Accepts connections from 4 clients.
- `broadcast_connect_4clients()`: Broadcasts connected client information.
- `receive_and_store_md5_data()`: Receives and stores MD5 data from clients.
- `broadcast_md5_info()`: Broadcasts MD5 information to clients.
- `receive_chunk_info()`, `receive_complete_info()`: Receives chunk and complete file information from clients.

**Global Variables:**
- `system_clock`, `start_time`, `end_time`, `MAX_CLIENTS`, `chunk_size`, `client_sockets`, etc.

**Other Variables:**
- Various other variables for tracking client connections, time, and data.

### 📘Client.py Components

**Functions:**
- `received_broadcasting_client_data()`, `calculate_file_md5()`, `connect_between_clients()`, `send_data()`, `received_data()`, etc.
- Handles file MD5 calculation, client-to-client connections, and data transmission.

**Global Variables:**
- `server_ip`, `server_port`, `client_ip`, `client_port`, `system_clock`, `chunk_size`, etc.

**Other Variables:**
- Variables for managing time, client info, MD5 data, socket communication, etc.

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
