import socket
from threading import Thread
import json
from dataformat import *

clientList = []  # 서버에 접속한 클라이언트 목록

# 쓰레드에서 실행되는 코드입니다.
# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다.
def socket_thread(client, addr):
    print(f'\n>> Connected by : [{addr}]')
    print(f'>> Current Sockets : {len(clientList)}')
    recivedData = json.loads(client.recv(1024).decode())
    # print(f'{recivedData}')
    # 커넥션 시 데이터 업데이트 및 메시징 초기화

    UPDATE_ECRARM_STATUS(ECRARM_STATUS,
                         IP=str(addr), FROM=recivedData["from"],
                         TYPE="connect", DATA=True, updatingStatus=recivedData["status"])
    for currentClient in clientList:
        currentClient.send(SEND_STATUS(ECRARM_STATUS).encode())
    recivedData = ""
    print(f'>> waiting socket connections ....\n\n')
    # 클라이언트가 접속을 끊을 때 까지 반복합니다.

    while True:
        # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
        try:
            tempData = client.recv(1024)
            if not tempData:
                raise ConnectionResetError()
            recivedData = json.loads(tempData.decode())
        except json.JSONDecodeError as e:
            print(e)
            print("잘못된 정보를 수신하였습니다.")
            recivedData=""
            continue
        except ConnectionResetError as e:
            if client in clientList:
                clientList.remove(client)
                print(f'>> \nDisconnected by [{addr}]')
                print(f'>> Current Sockets : {len(clientList)}')
                DISCONNECT_AND_STATUS_UPDATE(ECRARM_STATUS, str(addr))
                for currentClient in clientList:
                    currentClient.send(SEND_STATUS(ECRARM_STATUS).encode())
            print(f'>> Waiting...\n\n')
            break

        else:
            # print(f'{recivedData}')
            UPDATE_ECRARM_STATUS(ECRARM_STATUS,
                                 IP=str(addr), FROM=recivedData["from"], TYPE="data",
                                 DATA=recivedData["data"], updatingStatus=recivedData["status"])
            # 서버에 접속한 클라이언트들에게 브로드캐스팅
            for currentClient in clientList:
                currentClient.send(SEND_STATUS(ECRARM_STATUS).encode())


# 서버 커맨드
def _command_():
    while True:
        inputData = input('')
        if inputData == 'close':
            print("exit server")
            break
        elif inputData == 'status':
            SHOW_ECRARM_STATUS(ECRARM_STATUS)
        elif inputData == 'init':
            INITIALIZE_DATA_STATUS(ECRARM_STATUS)
            for currentClient in clientList:
                currentClient.send(SEND_STATUS(ECRARM_STATUS).encode())
        else:
            print(">> no command")


# 서버 IP 및 열어줄 포트
# HOST = '155.230.25.98'
# HOST = '127.0.0.1'
HOST = '192.168.0.15'
PORT = 9999

if (__name__ == "__main__"):
    try:
        # 서버 소켓 생성
        print('>> Server Start')
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        # 서버 커맨드 쓰레드 생성
        print('>> Waiting...\n\n')
        serverCommand = Thread(name="serverCommand",
                               target=_command_, args=(), daemon=True)
        serverCommand.start()
        while True:
            # 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.
            client, addr = server.accept()
            clientList.append(client)
            # 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다.
            socketServer = Thread(
                name="socketServer", target=socket_thread, args=(client, addr), daemon=True)
            socketServer.start()

    except Exception as e:
        print('에러는? : ', e)
    except KeyboardInterrupt:
        print('강제종료')
    finally:
        server.close()
