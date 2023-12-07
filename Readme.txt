* 5조
- 박민수 20193060 : 코드 작성 및 서류 작업
- 이수민 20193081 : 코드 작성 및 AWS 연결
- 이동영 20193076 : 코드 작성 및 서류 작업

[Server.py]

* 프로그램 구성요소 설명
- 함수
 - accept_4clients_connection() : 서버 스레드 하나 당 클라이언트 4개와 통신하기 위해, 4개의 연결을 받는 함수
 - broadcast_connect_4clients() : 서버에서 클라이언트에게 연결된 모든 클라이언트의 정보(ip, port)를 전송하는 함수
 - receive_and_store_md5_data() : 클라이언트로부터 MD5 데이터를 수신하고 해당 데이터를 저장하는 함수
 - broadcast_md5_info() : 서버에서 클라이언트에게 연결된 모든 클라이언트의 ip, port, MD5 정보를 전송하는 함수
 - receive_chunk_info() : 클라이언트로부터 청크 정보를 수신하는 함수
 - receive_complete_info() : 클라이언트로부터 전체 정보를 수신하는 함수
 - main() : 프로그램의 메인 루틴을 수행하는 함수로, 클라이언트와의 연결, 데이터 송수신, 정보 전달 등을 관리하는 함수

- 전역변수
 - system_clock : 각 연산 당 1씩 증가하는 시스템 초를 저장하는 변수
 - start_time, end_time : 프로그램 시작 시간과 종료 시간을 저장하는 변수
 - MAX_CLIENTS : 연결할 클라이언트들의 최대 개수를 나타내는 변수
 - chunk_size : 데이터 전송 시 사용되는 청크의 크기를 나타내는 변수
 - client_sockets : 연결된 클라이언트들의 소켓을 저장하는 리스트
 - client_ips, client_ports : 각 클라이언트의 IP 주소와 포트 번호를 저장하는 리스트
 - connected_client_list : 연결된 클라이언트들의 정보를 저장하는 리스트
 - c1_md5_list, c2_md5_list, c3_md5_list, c4_md5_list : 각 클라이언트의 MD5 해시 값을 저장하는 리스트
 - server : 서버 소켓을 나타내는 변수

- 변수
 - client_accept_cnt: 클라이언트 연결 수를 추적하기 위한 변수
 - current_time: 현재 시간을 밀리초로 저장하는 변수
 - time_difference: 시간의 차이를 계산하여 저장하는 변수
 - formatted_time: 형식화된 시간 정보를 저장하는 변수
 - microsecond: 밀리초에서 남은 부분(마이크로초)을 저장하는 변수
 - listen: 서버 수신 대기 중인 메시지를 저장하는 변수
 - accept: 클라이언트 연결 수락 메시지를 저장하는 변수
 - start_time: 서버 시작 시간을 저장하는 변수
 - broadcast_client_list: 브로드캐스트할 연결된 클라이언트 목록을 저장하는 변수
 - send_msg: 브로드캐스트할 메시지를 저장하는 변수
 - client_info_md5_data: 클라이언트로부터 수신한 MD5 데이터를 저장하는 변수
 - ip_addr, port_num: 클라이언트의 IP 주소와 포트 번호를 저장하는 변수
 - client_info: 클라이언트 정보를 저장하는 변수
 - c_md5: 클라이언트로부터 수신한 MD5 체크섬을 저장하는 변수

[client.py]

* 프로그램 구성요소 설명
- 함수
 - received_broadcasting_client_data(c_socket, f) : 클라이언트가 브로드캐스팅된 데이터를 수신하는 함수
 - calculate_file_md5(f_path) : 파일의 MD5 해시를 계산하는 함수
 - connect_between_clients(c_ip, c_port, f) : 서로 다른 클라이언트 간에 연결을 수립하는 함수
 - send_data(c_socket, f_path, f) : 파일 데이터를 다른 클라이언트에게 전송하는 함수
 - received_data(c_socket, f_path, f) : 다른 클라이언트로부터 데이터를 수신하는 함수
 - calculate_md5_for_files_in_directory(directory) : 디렉토리 내 파일들의 MD5 값을 계산하여 딕셔너리로 반환하는 함수
 - main() : 클라이언트의 주요 동작을 수행하는 함수

- 전역변수
 - server_ip, server_port : 서버의 IP 주소와 포트 번호를 저장하는 변수
 - client_ip, client_port : 현재 클라이언트의 IP 주소와 포트 번호를 저장하는 변수
 - system_clock, start_time, end_time : 시스템의 클럭 정보 및 프로그램 시작 및 종료 시간을 저장하는 변수
 - chunk_size : 파일 전송 시 사용되는 청크 크기를 저장하는 변수
 - file_path : 클라이언트가 전송할 파일의 경로를 저장하는 변수
 - file_collection : 클라이언트가 소유한 파일의 목록을 저장하는 변수
 - connected_s_client_socket_list, connected_r_client_socket_list : 연결된 송신 클라이언트 소켓과 수신 클라이언트 소켓 목록을 저장하는 변수
 - connected_client_ip_list, connected_client_port_list : 연결된 클라이언트의 IP 주소와 포트 번호 목록을 저장하는 변수
 - having_md5_list, having_chunk_list1, having_chunk_list2, having_chunk_list3 : 클라이언트가 가지고 있는 MD5 및 청크 정보 목록을 저장하는 변수
 - client_socket : 클라이언트의 소켓을 저장하는 변수

- 변수
 - current_time : 현재 시간을 밀리초로 저장하는 변수
 - time_difference : 시간의 차이를 계산하여 저장하는 변수
 - formatted_time : 형식화된 시간 정보를 저장하는 변수
 - received_client_info : 서버로부터 수신한 클라이언트 정보를 저장하는 변수
 - file: 전송할 파일을 열고 읽기 위한 파일 객체
 - chunk : 파일에서 읽은 청크
 - data : 클라이언트로부터 수신한 데이터
 - md5_dict : 파일명과 해당 파일의 MD5 해시를 저장하는 딕셔너리
 - md5 : 파일의 MD5 해시
 - client_info : 클라이언트 정보
 - client_info_md5_data : 클라이언트 정보와 MD5 데이터
 - received_md5_info : 서버로부터 수신한 MD5 정보
 - c1_socket : 소켓을 생성하고 바인드
 - matches : 정규 표현식으로 매칭된 결과
 - ip_addr, port_num, md5_value : 매칭 결과에서 추출한 값들
 - new_client_socket, new_client_address : 새로운 클라이언트와의 소켓 및 주소
 - c1_send_threads, c1_receive_threads : 전송 및 수신 스레드
 - st, r t : 전송 및 수신 스레드
 - download_file_path : 다운로드 받은 파일을 저장하는 경로
 - md5_results : 디렉토리 내 파일들의 MD5 값을 저장하는 딕셔너리
 - file_name, md5_value : 파일명과 해당 파일의 MD5 해시

[소스코드 컴파일 방법]
Python 언어로 작성된 소스 코드이기 때문에 별도의 컴파일 과정이 필요하지 않습니다. 소스 코드에 맞는 Python 버전(3.9 이상)과 적절한 IDE이 필요합니다.


[프로그램 실행환경 및 실행방법 설명]

* 프로그램 실행환경
- Python 버전 3.9 & Pycharm community edition 버전 2023.2.3
- aws ec2 인스턴스(ubuntu)

* 프로그램 실행방법
- EC2 인스턴스에서는 server.py, client1.py, client2.py 실행 후, 로컬에서는 PyCharm을 통해 client3.py 및 client4.py를 실행

[구현한 최적의 알고리즘 제시 및 설명]
# Step 1: 서버가 클라이언트와 연결하면서 클라이언트의 IP와 포트 정보를 수집
server.connect4Clients()

# Step 2: 서버는 클라이언트의 IP와 포트 정보를 묶어서 다시 클라이언트에게 송신
connectedClientsInfo = server.getConnectedClientsInfo()
server.sendTo4Clients(connectedClientsInfo)

# Step 3: 클라이언트는 자신의 .file의 MD5 값을 서버에 송신
client.sendFileMD5ToServer()

# Step 4: 서버는 클라이언트 정보(ip,port)와 파일 MD5 값을 모든 클라이언트에 뿌려줌
allClientsInfo = server.getAllClientsInfoWithFileMD5()
server.sendTo4Clients(allClientsInfo)

# Step 5: 클라이언트는 자신이 가지고 있지 않은 MD5 값을 가진 클라이언트에게 파일을 요청하고,
#         자신이 가지고 있는 MD5 값을 상대 클라이언트에게 송신
for eachClientInfo in allClientsInfo:
    if client.hasFileMD5(eachClientInfo.fileMD5) is False:
        client.requestFileFromOtherClient(eachClientInfo.ip, eachClientInfo.port)
    if client.hasFileMD5(eachClientInfo.fileMD5) and \
            eachClientInfo.ip != client.getOwnIP() and \
            eachClientInfo.port != client.getOwnPort():
        client.sendOwnFileMD5ToOtherClient(eachClientInfo.ip, eachClientInfo.port)


[Error or Additional Message Handling에 대한 사항 설명]
- ConnectionReset Error : "Client 1: Connection was forcibly closed."라는 메시지를 출력하고 프로그램이 종료
- KeyboardInterrupt :  "Client 1: Connection closed"라는 메시지를 출력하고 프로그램이 종료

[Additional Comments: 추가로 과제제출관련 언급할 내용 작성]
- 다른 환경에서의 통신이 이루어지기 때문에 외부 서버에서의 접근에 대한 허용이 필요( ex)포트포워딩 )

