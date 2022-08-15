import React, { useEffect, useState, useRef } from "react";

const SocketTest = () => {
  const [socketConnected, setSocketConnected] = useState(false);
  const [sendMsg, setSendMsg] = useState(false);
  const [isDetectionRunning, setDetectionRunning] = useState(false);
  const [items, setItems] = useState([]);

  const webSocketUrl = `ws://localhost:8888`;
  let ws = useRef(null);

  const startButtonClickHandler = () => {
    if (socketConnected) {
      ws.current.send(
        JSON.stringify({
          id: "WEB",
          message: "Start",
        })
      );
      setDetectionRunning(true);
    }
  };
  const stopButtonClickHandler = () => {
    if (socketConnected) {
      ws.current.send(
        JSON.stringify({
          id: "WEB",
          message: "Stop",
        })
      );
      setDetectionRunning(false);
    }
  };
  // 소켓 객체 생성
  useEffect(() => {
    if (!ws.current) {
      ws.current = new WebSocket(webSocketUrl);
      ws.current.onopen = () => {
        console.log("connected to " + webSocketUrl);
        setSocketConnected(true);
        setSendMsg("CONNECTED");
      };
      ws.current.onclose = (error) => {
        console.log("disconnect from " + webSocketUrl);
        console.log(error);
      };
      ws.current.onerror = (error) => {
        console.log("connection error " + webSocketUrl);
        console.log(error);
      };
      ws.current.onmessage = (evt) => {
        const data = JSON.parse(evt.data);
        console.log(data);
        setItems((prevItems) => [...prevItems, data]);
      };
    }

    return () => {
      console.log("clean up");
      ws.current.close();
    };
  }, []);

  // 소켓이 연결되었을 시에 send 메소드
  useEffect(() => {
    if (socketConnected) {
      ws.current.send(
        JSON.stringify({
          message: sendMsg,
        })
      );

      setSendMsg(true);
    }
  }, [socketConnected]);

  return (
    <>
      <div>socket connected : {`${socketConnected}`}</div>
      <div>res : </div>
      <div>
      {!isDetectionRunning ? (
          <button onClick={startButtonClickHandler}>start</button>
        ) : (
          <button onClick={stopButtonClickHandler}>stop</button>
        )}
        {items.map((item, index) => {
          return <div key={index}>{JSON.stringify(item)}</div>;
        })}

      </div>
    </>
  );
};

export default SocketTest;
