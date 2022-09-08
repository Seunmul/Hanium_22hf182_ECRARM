import React from "react";

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
  return (
    <div style={style}>
      <div>
        <h1>Detail Data : </h1>
        <h5>WebSocketConnection : {String(webSocketConnect)} - {String(webSocketConnectionStatus)}</h5>
        <h5>System Status : {String(receivedData.status)}</h5>
        <strong>
          {JSON.stringify(receivedData)}
        </strong>
      </div>
      <Button onClick={()=>dispatch(clearReceivedDataList())}> clear log </Button>
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
        
        {receivedDataList.map((item, index) => {
          return <div key={index}>{JSON.stringify(item)}</div>;
        })}
      </div>
    </div>
  )
};

export default Detail;
