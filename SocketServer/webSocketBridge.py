import websockets
import asyncio
import json

SOCKET_HOST = '127.0.0.1'
# SOCKET_HOST = '155.230.25.98'
SOCKET_PORT = 9999

WEBSOCKET_HOST = '127.0.0.1'
# WEBSOCKET_HOST = '155.230.25.98'
WEBSOCKET_PORT = 8888

WEB_CLIENTS = []  # 서버에 접속한 클라이언트 목록

# 시스템 스테이터스 전역변수 선언
global system_status
system_status = "initializing"
global prevManualData
prevManualData = ""


async def socket_to_web(websocket, reader, writer):
    # 시스템 스테이터스 전역변수 사용
    global system_status
    # 루프를 돌면서 입력받은 내용을 서버로 보내고,
    # 응답을 받으면 출력합니다.
    while True:
        try:
            # 서버로부터 받은 응답을 표시
            tempData = await reader.read(1024)  # type
            # 받은 메세지가 없으면 루프 해제.
            if not tempData:
                raise websockets.exceptions.ConnectionClosedError(" ", " ")
            receivedData = json.loads(tempData)
        except json.JSONDecodeError as e:
            print(e)
            print("잘못된 정보를 수신하였습니다.")
            receivedData = ""
            continue
        # print(f"\n[StW] received: {len(receivedData)} bytes")
        # print(f"\n>> [StW] receivedData: {receivedData}")
        system_status = receivedData["status"]
        print(f">> [StW] system status : {system_status}")
        await websocket.send(json.dumps(receivedData))


async def web_to_socket(websocket, reader, writer):
    # 시스템 스테이터스 전역변수 사용
    global system_status
    global prevManualData
    
    # 웹에서 온 응답을 소켓으로 전송하는 async 함수
    async for receivedData in websocket:
        # print(f"\n[WtS] received: {len(receivedData)} bytes")
        data = json.loads(receivedData)["data"]
        # print(data)
        if (data == "connect"):
            sendingData = json.dumps({
                "ip": websocket.remote_address,
                "from": "Web",
                "status": "connect",
                "data": ""
            }, sort_keys=True, indent=4)
            
        elif (system_status == "waiting" and data == "start"):
            sendingData = json.dumps({
                "ip": websocket.remote_address,
                "from": "Web",
                "status": "starting",
                "data": ""
            }, sort_keys=True, indent=4)
            
        elif (system_status != "waiting" and data == "stop"):
            sendingData = json.dumps({
                "ip": websocket.remote_address,
                "from": "Web",
                "status": "stopping",
                "data": ""
            }, sort_keys=True, indent=4)
            
        elif (system_status == "waiting" and data == "manual"):
            sendingData = json.dumps({
                "ip": websocket.remote_address,
                "from": "Web",
                "status": "manual",
                "data": ""
            }, sort_keys=True, indent=4)
            
        elif (system_status == "manual" and data =="waiting"):
            sendingData = json.dumps({
                "ip": websocket.remote_address,
                "from": "Web",
                "status": "waiting",
                "data": prevManualData
            }, sort_keys=True, indent=4)
            
        elif (system_status == "manual"):
            sendingData = json.dumps({
                "ip": websocket.remote_address,
                "from": "Web",
                "status": "manual",
                "data": json.loads(data)
            }, sort_keys=True, indent=4)
            prevManualData = json.loads(data)
            
        else:
            sendingData = json.dumps({
                "ip": websocket.remote_address,
                "from": "Web",
                "status": "undefined case",
                "data": data
            }, sort_keys=True, indent=4)
            print("\n>>[WtS] undefined web message")

        print(f"\n>> [WtS] sendingData: {sendingData}")
        writer.write(sendingData.encode())
        # await websocket.send(sendingData)  # echo


async def webSocketClosedHandler(websocket, writer):
    status = await websocket.wait_closed()
    # print(status)
    if (not status):
        writer.close()
        await writer.wait_closed()


async def handler(websocket):
    try:
        print(websocket.remote_address)
        print(">> [C] Websocket connected")
        # 소켓서버와의 연결을 생성합니다.
        reader: asyncio.StreamReader
        writer: asyncio.StreamWriter
        reader, writer = await asyncio.open_connection(str(SOCKET_HOST), int(SOCKET_PORT))
        print(">> [C] Socket connected")
        WEB_CLIENTS.append(websocket.remote_address)
        print(f'>> Current WEB_CLIENTS : {len(WEB_CLIENTS)}\n')
        # asyncio와 쓰레드를 이용하여, 소켓서버와 웹소켓 서버로 부터 오고가는 데이터를 중계합니다.
        await asyncio.gather(
            await asyncio.to_thread(socket_to_web, websocket, reader, writer,),
            await asyncio.to_thread(web_to_socket, websocket, reader, writer,),
            await asyncio.to_thread(webSocketClosedHandler, websocket, writer,)
        )
    except websockets.exceptions.ConnectionClosedOK as e:
        print(f'>> 새로고침되었습니다. IP : {str(websocket.remote_address)}')
        print(e)
    except websockets.exceptions.ConnectionClosedError as e:
        WEB_CLIENTS.remove(websocket.remote_address)
        print(f'>> Disconnected, IP : {str(websocket.remote_address)}')
        print(f'>> Current WEB_CLIENTS : {len(WEB_CLIENTS)}\n')

async def main():
    # 웹소켓 서버 이용자가 요청을 보내면 handler가 인식합니다.
    async with websockets.serve(handler, WEBSOCKET_HOST, WEBSOCKET_PORT):
        await asyncio.Future()  # run forever
print(">> Connect....")
try:
    asyncio.run(main())
except KeyboardInterrupt as e:
    print("강제종료")


# print(websocket.id)
# print(websocket.wait_closed)
