import websockets
import asyncio
import json

SOCKET_HOST = '155.230.25.98'
SOCKET_PORT = 9999

WEBSOCKET_HOST = '155.230.25.98'
WEBSOCKET_PORT = 8888

WEB_CLIENTS = []  # 서버에 접속한 클라이언트 목록

# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리


async def socket_to_web(websocket, reader, writer):
    # 루프를 돌면서 입력받은 내용을 서버로 보내고,
    # 응답을 받으면 출력합니다.
    while True:
        # 서버로부터 받은 응답을 표시
        receivedData = await reader.read(1024)  # type
        if not receivedData:  # 받은 메세지가 없으면 루프 해제.
            raise websockets.exceptions.ConnectionClosedError(" ", " ")
        print(f"\n[StW] received: {len(receivedData)} bytes")
        print(f"[StW] receivedData: {receivedData.decode()}")
        await websocket.send(receivedData.decode())


async def web_to_socket(websocket, reader, writer):
    async for receivedData in websocket:
        print(f"\n[WtS] received: {len(receivedData)} bytes")
        # tempData = json.loads(receivedData)
        # print(tempData)
        sendingData = json.dumps({
            "ip": websocket.remote_address,
            "from": "Web",
            "data": json.loads(receivedData)["data"]
        }, sort_keys=True, indent=4)
        print(f"[WtS] receivedData: {sendingData}")
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
