import socket
from threading import Thread
import json
from dataformat import *

clientList = []  # 서버에 접속한 클라이언트 목록
# 쓰레드에서 실행되는 코드입니다.
# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다.


def socket_threaded(client, addr):
    print(f'\n>> Connected by : [{addr}]')
    print(f'>> Current Sockets : {len(clientList)}')
    recivedData = json.loads(client.recv(1024).decode())
    print(f'{recivedData}')
    UPDATE_ECRARM_STATUS(ECRARM_STATUS,
                         str(addr), recivedData["from"], recivedData["data"], True)
    recivedData = ""
    print(f'>> Waiting...\n\n')
    for currentClient in clientList:
        currentClient.send(SEND_STATUS(ECRARM_STATUS).encode())
    # 클라이언트가 접속을 끊을 때 까지 반복합니다.
    try:
        while True:
            # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
            recivedData = client.recv(1024)
            if not recivedData:
                raise ConnectionResetError()
            tempData = json.loads(recivedData.decode())

            if (tempData["from"] == "Controller"):
                sendingData = json.dumps({
                    "ip": [str(addr[0]), addr[1]],
                    "from": tempData["from"],
                    "data": tempData["data"]
                }, sort_keys=True, indent=4)
            elif (tempData["from"] == "Detector"):
                sendingData = json.dumps({
                    "ip": [str(addr[0]), addr[1]],
                    "from": tempData["from"],
                    "data": tempData["data"]
                }, sort_keys=True, indent=4)
            elif (tempData["from"] == "Web"):
                sendingData = json.dumps({
                    "ip": tempData["ip"],
                    "from": tempData["from"],
                    "data": tempData["data"]
                }, sort_keys=True, indent=4)
            UPDATE_ECRARM_STATUS(ECRARM_STATUS,
                                 str(addr), tempData["from"], "data", tempData["data"])

            # 서버에 접속한 클라이언트들에게 브로드캐스팅
            for currentClient in clientList:
                if currentClient != client:
                    currentClient.send(SEND_STATUS(ECRARM_STATUS).encode())

    except ConnectionResetError as e:
        if client in clientList:
            clientList.remove(client)
            print(f'>> \nDisconnected by [{addr}]')
            print(f'>> Current Sockets : {len(clientList)}')
            DISCONNECT_AND_STATUS_UPDATE(ECRARM_STATUS, str(addr))
            for currentClient in clientList:
                currentClient.send(SEND_STATUS(ECRARM_STATUS).encode())
            print(f'>> Waiting...\n\n')

# 서버 커맨드


def server_command():
    while True:
        inputData = input('')
        if inputData == 'close':
            print("exit server")
            break
        elif inputData == 'status':
            SHOW_ECRARM_STATUS(ECRARM_STATUS)
        elif inputData == 'initialize':
            INITIALIZE_DATA_STATUS(ECRARM_STATUS)


# 서버 IP 및 열어줄 포트
HOST = '155.230.25.98'
# HOST = '127.0.0.1'
PORT = 9999

try:
    # 서버 소켓 생성
    print('>> Server Start')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    # 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.
    # 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다.
    print('>> Waiting...\n\n')
    serverCommand = Thread(name="serverCommand",
                           target=server_command, args=(), daemon=True)
    serverCommand.start()
    while True:
        client, addr = server.accept()
        clientList.append(client)
        socketServer = Thread(
            name="socketServer", target=socket_threaded, args=(client, addr), daemon=True)
        socketServer.start()

except Exception as e:
    print('에러는? : ', e)
except KeyboardInterrupt:
    print('강제종료')
finally:
    server.close()
