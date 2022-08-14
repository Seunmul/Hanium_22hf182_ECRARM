import socket
from _thread import *
client_sockets = [] # 서버에 접속한 클라이언트 목록

# 쓰레드에서 실행되는 코드입니다.
# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다.
def threaded(client_socket, addr):
    print('>> Connected by :', addr[0], ':', addr[1])

    # 클라이언트가 접속을 끊을 때 까지 반복합니다.
    while True:

        try:

            # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
            data = client_socket.recv(1024)

            if not data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break

            print('>> Received from ' + addr[0], ':', addr[1], data.decode())

            # 서버에 접속한 클라이언트들에게 채팅 보내기
            # 메세지를 보낸 본인을 제외한 서버에 접속한 클라이언트에게 메세지 보내기
            for client in client_sockets :
                if client != client_socket :
                    client.send(data)

        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            break

    if client_socket in client_sockets :
        client_sockets.remove(client_socket)
        print('remove client list : ',len(client_sockets))

    client_socket.close()


# 서버 IP 및 열어줄 포트
HOST = '127.0.0.1'
PORT = 9999

# 서버 소켓 생성
print('>> Server Start')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

# 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.

# 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다.

# 서버에서 클라이언트로 보내는 메세지
def send_srv_msg():
    if len(client_sockets)==0:
        return
    data = client_socket.recv(1024)
    print("\n[from client] recived : ",repr(data.decode()),end="\n")
    
    if data.decode()=='closed, press any key':
        server_socket.close()
        
    message = input('send message : ')
    for client in client_sockets :
        client.send(message.encode())
    
try:
    # print('>> Wait')
    # client_socket, addr = server_socket.accept()
    # client_sockets.append(client_socket)
    # print("참가자 수 : ", len(client_sockets))
    while True:
        # send_srv_msg()
        print("processing task -- \n")
        
        print('>> Wait')
        client_socket, addr = server_socket.accept()
        client_sockets.append(client_socket)
        start_new_thread(threaded, (client_socket, addr))
        print("참가자 수 : ", len(client_sockets))
except Exception as e :
    print ('에러는? : ',e)

finally:
    server_socket.close()

