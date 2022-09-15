<<<<<<< HEAD:Web_control_interface/react_front/src/websocket/websocket.js
import React, { useEffect, useState, useRef } from "react";
import { Button } from "react-bootstrap";
import { useSelector, useDispatch } from 'react-redux'
import {
  connected, disconnected, updateWebSocketConnection
  , updateSystemStatus, updateReceivedDataList
} from "../reducer/websocketReducer";

const WebSocketComponent = () => {

  const [webSocketStatusMsg, setWebSocketStatusMsg] = useState("");
  const [isDataReceived, setIsDataReceived] = useState(false);
  const webSocketConnect = useSelector(state => state.websocket.connect)
  const webSocketConnectionStatus = useSelector(state => state.websocket.connectionStatus)
  const receivedData = useSelector(state => state.websocket.data)
  
  const dispatch = useDispatch()

  const webSocketUrl = "ws://155.230.25.98:8888";
  const ws = useRef(null); //useRef ws객체 할당

  // websocket 연결 try
  const connectWebSocket = () => {
=======
import React, { useCallback, useEffect, useRef } from "react";

import { useSelector, useDispatch } from "react-redux";
import {
  updateSendingMessage,
  updateWebSocketConnection,
  updateSystemStatus,
  updateReceivedDataList,
  setIsDataReceived,
} from "../reducer/websocketReducer";

const WebSocketComponent = () => {
  // const webSocketConnectionStatus = useSelector(
  //   (state) => state.websocket.connectionStatus
  // );
  const sendingMessage = useSelector((state) => state.websocket.sendingMessage);
  const connectionHandleMsg = useSelector(
    (state) => state.websocket.connectionHandleMsg
  );

  const ws = useRef(null); //useRef ws객체 할당
  const webSocketUrl = "ws://155.230.25.98:8888";
  const dispatch = useDispatch();
  // const webSocketUrl = "ws://127.0.0.1:8888";

  // websocket 연결 try
  const webSocketHandler = useCallback(() => {
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/websocket/websocket.js
    console.log("---\nopen socket");
    ws.current = new WebSocket(webSocketUrl);

    ws.current.onopen = () => {
      console.log("connected to " + webSocketUrl);
<<<<<<< HEAD:Web_control_interface/react_front/src/websocket/websocket.js
      dispatch(connected())
      dispatch(updateWebSocketConnection(Number(ws.current.readyState)))

    };
    ws.current.onerror = (error) => {
      console.log("connection error " + webSocketUrl);
      dispatch(disconnected())
      dispatch(updateWebSocketConnection(Number(ws.current.readyState)))

=======
      dispatch(updateWebSocketConnection(Number(ws.current.readyState)));
      dispatch(updateSendingMessage("connect"));
    };
    ws.current.onerror = (error) => {
      console.log("connection error " + webSocketUrl);
      dispatch(updateWebSocketConnection(Number(ws.current.readyState)));
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/websocket/websocket.js
      console.log(error);
    };
    ws.current.onclose = (error) => {
      console.log("disconnect from " + webSocketUrl);
<<<<<<< HEAD:Web_control_interface/react_front/src/websocket/websocket.js
      dispatch(disconnected())
      dispatch(updateWebSocketConnection(Number(ws.current.readyState)))
=======
      dispatch(updateWebSocketConnection(Number(ws.current.readyState)));
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/websocket/websocket.js
      console.log(error);
    };
    ws.current.onmessage = (evt) => {
      const receivedData = JSON.parse(evt.data);
      console.log(receivedData);
<<<<<<< HEAD:Web_control_interface/react_front/src/websocket/websocket.js
      setIsDataReceived(true);
      dispatch(updateSystemStatus(receivedData))
      dispatch(updateReceivedDataList(receivedData))
    };
  };
  // 시작버튼 이벤트 핸들러
  const startButtonClickHandler = async () => {
    if (webSocketConnect && isDataReceived) {
      ws.current.send(
        JSON.stringify({
          data: "start",
        })
      );

      setIsDataReceived(false);
    }
  };
  // 멈춤버튼 이벤트 핸들러
  const stopButtonClickHandler = async () => {
    if (webSocketConnect && isDataReceived) {
      // print(ws.current.onmessage)
      await ws.current.send(
        JSON.stringify({
          data: "stop",
        })
      );
      setIsDataReceived(false);
    }
  };
  // 소켓 열기 버튼 이벤트 핸들러
  const openButtonClickHandler = () => {
    if (webSocketConnectionStatus === ws.current.CLOSED) connectWebSocket();
  };
  // 소켓 닫기 버튼 이벤트 핸들러
  const closeButtonClickHandler = () => {
    if (webSocketConnectionStatus === ws.current.OPEN) {
      console.log("close socket");
      ws.current.close();
    }
  };
=======
      dispatch(setIsDataReceived(true));
      dispatch(updateSystemStatus(receivedData));
      dispatch(updateReceivedDataList(receivedData));
    };
  }, [dispatch]);
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/websocket/websocket.js

  // 첫 화면 로딩 시 소켓 객체 생성
  useEffect(() => {
    if (!ws.current) {
<<<<<<< HEAD:Web_control_interface/react_front/src/websocket/websocket.js
      connectWebSocket()
=======
      webSocketHandler();
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/websocket/websocket.js
    }
    return () => {
      console.log("clean up");
      ws.current.close();
    };
<<<<<<< HEAD:Web_control_interface/react_front/src/websocket/websocket.js
  }, []);

  // 소켓 연결 상태별 메소드 설정
  useEffect(() => {
    if (ws.current) {
      switch (webSocketConnectionStatus) {
        case ws.current.CONNECTING: //webSocketConnectionStatus === 0
          setWebSocketStatusMsg("connecting");
          break;
        case ws.current.OPEN:
          setWebSocketStatusMsg("open : connected");
          ws.current.send(
            JSON.stringify({
              data: "connect",
            })
          );
          break;
        case ws.current.CLOSING:
          setWebSocketStatusMsg("closing");
          break;
        case ws.current.CLOSED:
          setWebSocketStatusMsg("not connected");
          break;
        default:
          setWebSocketStatusMsg("something wrong, error");
          break;
      }
      return () => {
        console.log("connection updated");
      };
    }

  }, [webSocketConnectionStatus]);

  const systemControlButton =
    webSocketConnect && (receivedData.status === "waiting" || receivedData.status === "initializing") ? (
      <button style={{ color: "blue" }} onClick={startButtonClickHandler}>
        start
      </button>
    ) : (
      <button style={{ color: "red" }} onClick={stopButtonClickHandler}>
        stop
      </button>
    );

  return (

    <>
      <div>
        
      </div>
      <hr></hr>
      <Button className="my-2" onClick={openButtonClickHandler}>
        open socket
      </Button>
      <Button className="my-2" onClick={closeButtonClickHandler}>
        close socket
      </Button>
      <hr></hr>
      <div>Status : {`connection-${webSocketStatusMsg} , system status-${receivedData.status}`}</div>
      <div>res : </div>
      {webSocketConnect && systemControlButton}
    </>

  );
=======
  }, [webSocketHandler]);

  // 웹 소켓 연결 버튼 관련 로직
  useEffect(() => {
    if (
      ws.current.readyState === ws.current.CLOSED &&
      connectionHandleMsg === "open"
    ) {
      webSocketHandler();
    } else if (
      ws.current.readyState === ws.current.OPEN &&
      connectionHandleMsg === "close"
    ) {
      console.log("---\n close socket")
      ws.current.close();
    }
  }, [webSocketHandler, connectionHandleMsg]);

  // 웹 소켓 서버에 메세지 보내는 로직
  useEffect(() => {
    if (ws.current && ws.current.readyState === ws.current.OPEN) {
      ws.current.send(
        JSON.stringify({
          data: String(sendingMessage),
        })
      );
      console.log(`sended to websocket server : ${sendingMessage}`);
    }
  }, [sendingMessage]);

  return <></>;
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/websocket/websocket.js
};

export default WebSocketComponent;
