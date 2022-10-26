import React from "react";

import { useSelector, useDispatch } from "react-redux";
// import { decrement, increment, incrementByAmount } from "../../reducer/counterReducer"
import { clearReceivedDataList } from "components/Util/reducer/websocketReducer";
import { Spinner, Button } from "react-bootstrap";
import "stylesheets/Detail.css";

const Detail = ({ style }) => {
  const webSocketConnect = useSelector((state) => state.websocket.connect);
  const webSocketConnectionStatus = useSelector(
    (state) => state.websocket.connectionStatus
  );
  const receivedData = useSelector((state) => state.websocket.data);
  const receivedDataList = useSelector(
    (state) => state.websocket.receivedDataList
  );
  const dispatch = useDispatch();
  return (
    <div style={style}>
      <div>
        <h1>Detail Data : </h1>
        <h4>
          WebSocketConnection : {String(webSocketConnect)} -{" "}
          {String(webSocketConnectionStatus)}
        </h4>

        <h4>
          System Status : {String(receivedData.status)}{" "}
          <Spinner animation="border" variant="primary" />
        </h4>

        {JSON.stringify(receivedData, null, 10)}
      </div>
      <div className="dash-button-area">
        <Button onClick={() => dispatch(clearReceivedDataList())}>
          {" "}
          clear log{" "}
        </Button>
      </div>
      <div className="detail-row">progress</div>

      <div>
        {receivedDataList.map((item, index) => {
          return <div key={index}>{JSON.stringify(item.status, null, 10)}</div>;
        })}
      </div>
    </div>
  );
};

export default Detail;
