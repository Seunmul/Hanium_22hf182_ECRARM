import React from "react";

<<<<<<< HEAD:Web_control_interface/react_front/src/components/main/Detail.js
import { useSelector,useDispatch } from 'react-redux'
// import { decrement, increment, incrementByAmount } from "../../reducer/counterReducer"
import { clearReceivedDataList } from "../../reducer/websocketReducer";
import { Spinner, ProgressBar, Button } from "react-bootstrap";
import './Detail.css'

const Detail = ({ style }) => {
  const webSocketConnect = useSelector(state => state.websocket.connect)
  const webSocketConnectionStatus = useSelector(state => state.websocket.connectionStatus)
  const receivedData = useSelector(state => state.websocket.data)
  const receivedDataList = useSelector(state => state.websocket.receivedDataList)
  const dispatch = useDispatch()
=======
import { useSelector, useDispatch } from "react-redux";
// import { decrement, increment, incrementByAmount } from "../../reducer/counterReducer"
import { clearReceivedDataList } from "../../reducer/websocketReducer";
import { Spinner, ProgressBar, Button } from "react-bootstrap";
import "./Detail.css";

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
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/main/Detail.js
  return (
    <div style={style}>
      <div>
        <h1>Detail Data : </h1>
<<<<<<< HEAD:Web_control_interface/react_front/src/components/main/Detail.js
        <h5>WebSocketConnection : {String(webSocketConnect)} - {String(webSocketConnectionStatus)}</h5>
        <h5>System Status : {String(receivedData.status)}</h5>
        <strong>
          {JSON.stringify(receivedData)}
        </strong>
      </div>
      <Button onClick={()=>dispatch(clearReceivedDataList())}> clear log </Button>
=======
        <h5>
          WebSocketConnection : {String(webSocketConnect)} -{" "}
          {String(webSocketConnectionStatus)}
        </h5>
        <h5>System Status : {String(receivedData.status)}</h5>
        
          {JSON.stringify( receivedData , null, 10)}
        
      </div>
      <div className="dash-button-area">
        <Button onClick={() => dispatch(clearReceivedDataList())}>
          {" "}
          clear log{" "}
        </Button>
      </div>
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/main/Detail.js
      <div>progress</div>
      <ProgressBar animated now={60} label={`${60}%`} />
      <div className="detail-row">
        <Spinner animation="border" variant="primary" />
        <Spinner animation="border" variant="secondary" />
        <Spinner animation="border" variant="success" />
        <Spinner animation="border" variant="danger" />
        <Spinner animation="border" variant="warning" />
        <Spinner animation="border" variant="info" />
        <Spinner animation="border" variant="light" />
        <Spinner animation="border" variant="dark" />
      </div>
      <div>
<<<<<<< HEAD:Web_control_interface/react_front/src/components/main/Detail.js
        
        {receivedDataList.map((item, index) => {
          return <div key={index}>{JSON.stringify(item)}</div>;
        })}
      </div>
    </div>
  )
=======
        {receivedDataList.map((item, index) => {
          return <div key={index}>{JSON.stringify(item.status,null,10)}</div>;
        })}
      </div>
    </div>
  );
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/main/Detail.js
};

export default Detail;
