import React, { useState, useEffect } from "react";
import useWebSocket from "react-use-websocket"; //웹소켓 라이브러리를 사용 합니다.

function Chatting(arg) {
  const [socketUrl] = useState(`ws://localhost:8888?${arg.id}`);
  const { sendMessage, lastMessage } = useWebSocket(socketUrl); //웹소캣 라이브러리인 useWebSocket 입니다.
  const [messageHistory, setMessageHistory] = useState([]); //웹소켓에서 메시지를 받으면 호출되는 상태 입니다.

  //메시지를 보내기 위한 기능 입니다.
  const [message, setMessage] = useState("");
  const onMessage = (event) => setMessage(event.target.value);
  const sendMsg = () => {
    let msg = {
      //전송 규격
      _room_id: "WEB",
      _id: "WEB",
      send: "send",
      message: message,
    };
    sendMessage(JSON.stringify(msg));
  };

  //메시지에 대한 변화에 대해서 정의 합니다.
  useEffect(() => {
    if (lastMessage !== null) {
      setMessageHistory((prev) => {
        //기존 메시지에 데이터를 추가합니다.
        let msg = lastMessage ? lastMessage.data : null;
        if (msg) {
          let object = JSON.parse(msg);
          lastMessage._id = object._id;
          lastMessage.result = object.result;
          lastMessage.message = object.message;
        }
        return prev.concat(lastMessage);
      });
    }
  }, [lastMessage, setMessageHistory]);

  //최초 방에 들어온 경우 실행되는 "나 방에 들어왔어" 기능 입니다.
  useEffect(() => {
    let join = {
      _room_id: "WEB",
      password: "PASSWORD",
      _id: "WEB",
      join: "join",
    };
    sendMessage(JSON.stringify(join));
  }, [sendMessage]);

  return (
    <div className="container">
      <div className="col-md-12 border m-4">
        chatting
        <input
          type="text"
          onChange={onMessage}
          value={message}
          placeholder="메시지를 입력하세요"
          className="form-control"
        />
        <button type="button" onClick={sendMsg} className="btn btn-success">
          {" "}
          send test
        </button>
      </div>

      <div className="col-md-12 border m-4">
        <div>전체 메시지</div>
        <ul>
          {messageHistory.map((message, idx) => {
            if (message.result) {
              let desc = "가 나갔습니다.";
              if (message.result === "someIn") {
                desc = "가 들어왔습니다.";
              }
              return (
                <div key={idx} className="form-control">
                  {message._id}
                  {desc}
                </div>
              );
            }
            return (
              <div key={idx} className="form-control">
                <strong>{message._id}</strong> : {message.message}
              </div>
            );
          })}
        </ul>
      </div>
    </div>
  );
}

export default Chatting;
