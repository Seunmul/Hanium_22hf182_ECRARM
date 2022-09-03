import React, { useEffect, useState, useRef } from "react";

const SocketTest = () => {
  const [socketConnected, setSocketConnected] = useState(false);
  const [recivedMsg, setRecivedMsg] = useState(false);
  const [sendMsg, setSendMsg] = useState(false);
  const [isDetectionRunning, setDetectionRunning] = useState(false);
  const [items, setItems] = useState([]);

  const webSocketUrl = `ws://192.168.0.13:8888`;
  let ws = useRef(null);

  const startButtonClickHandler = async () => {
    if (socketConnected && recivedMsg) {
      ws.current.send(
        JSON.stringify({
          id: "WEB",
          message: "Start",
        })
      );
      setDetectionRunning(true);
      setRecivedMsg(false);
    }
  };
  const stopButtonClickHandler = async () => {
    if (socketConnected && recivedMsg) {
      // print(ws.current.onmessage)
      await ws.current.send(
        JSON.stringify({
          id: "WEB",
          message: "Stop",
        })
      );
      setDetectionRunning(false);
      setRecivedMsg(false);
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
        const data = evt.data;
        console.log(data);
        setRecivedMsg((prev) => data);
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

  const detectionControlBtn =
    !isDetectionRunning && recivedMsg ? (
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
      <div>socket connected : {`${socketConnected}`}</div>
      <div>res : </div>
      <div>
        {socketConnected&&detectionControlBtn}
        {items.map((item, index) => {
          return <div key={index}>{JSON.stringify(item)}</div>;
        })}
      </div>
    </>
  );
};

export default SocketTest;
