import React from "react";
import { Badge, Container } from "react-bootstrap";
import { useSelector, useDispatch } from "react-redux";

import FirstRow from "./DashBoard/_first_row";
import SecondRow from "./DashBoard/_second_row";
import ThirdRow from "./DashBoard/_thrid_row";
import "stylesheets/DashBoard.css";

const DashBoard = ({ style }) => {
  const webSocketConnectionStatus = useSelector(
    (state) => state.websocket.connectionStatus
  );
  const receivedData = useSelector((state) => state.websocket.data);
  const isDataReceived = useSelector((state) => state.websocket.isDataReceived);
  const dispatch = useDispatch();

  let connectionStatusBadge = <div></div>;
  switch (webSocketConnectionStatus) {
    case 1:
      connectionStatusBadge = (
        <Badge bg="success me-2" style={{ fontSize: "15px" }}>
          connected
        </Badge>
      );
      break;
    case 2:
      connectionStatusBadge = (
        <Badge bg="warning me-2" style={{ fontSize: "15px" }}>
          connecting...
        </Badge>
      );
      break;
    default:
      connectionStatusBadge = (
        <Badge bg="danger me-2" style={{ fontSize: "15px" }}>
          not connected
        </Badge>
      );
      break;
  }
  let systemStatusBadge = <div></div>;
  switch (receivedData.status) {
    case "initializing":
      systemStatusBadge = (
        <Badge bg="secondary me-2" style={{ fontSize: "15px" }}>
          initializing...
        </Badge>
      );
      break;
    case "waiting":
      systemStatusBadge = (
        <Badge bg="success me-2" style={{ fontSize: "15px" }}>
          waiting...
        </Badge>
      );
      break;
    case "detecting":
      systemStatusBadge = (
        <Badge bg="warning me-2" style={{ fontSize: "15px" }}>
          detecting...
        </Badge>
      );
      break;
    case "detecting_finished":
      systemStatusBadge = (
        <Badge bg="warning me-2" style={{ fontSize: "15px" }}>
          detecting finished
        </Badge>
      );
      break;
    case "controlling":
      systemStatusBadge = (
        <Badge bg="primary me-2" style={{ fontSize: "15px" }}>
          controlling...
        </Badge>
      );
      break;
    case "controlling_finished":
      systemStatusBadge = (
        <Badge bg="primary me-2" style={{ fontSize: "15px" }}>
          controlling finished
        </Badge>
      );
      break;
    case "stopping":
      systemStatusBadge = (
        <Badge bg="danger me-2" style={{ fontSize: "15px" }}>
          stopping...
        </Badge>
      );
      break;
    case "manual":
      systemStatusBadge = (
        <Badge bg="info me-2" style={{ fontSize: "15px" }}>
          manual controlling mode...
        </Badge>
      );
      break;

    default:
      systemStatusBadge = (
        <Badge bg="danger me-2" style={{ fontSize: "15px" }}>
          error
        </Badge>
      );
      break;
  }

  const detectSystemStatusBadge = receivedData.Detector.connect ? (
    <Badge bg="success me-2" style={{ fontSize: "15px" }}>
      connected
    </Badge>
  ) : (
    <Badge bg="danger me-2" style={{ fontSize: "15px" }}>
      not connected
    </Badge>
  );
  const controlSystemStatusBadge = receivedData.Controller.connect ? (
    <Badge bg="success me-2" style={{ fontSize: "15px" }}>
      connected
    </Badge>
  ) : (
    <Badge bg="danger me-2" style={{ fontSize: "15px" }}>
      not connected
    </Badge>
  );

  return (
    <Container fluid style={style}>
      <FirstRow
        connectionStatusBadge={connectionStatusBadge}
        systemStatusBadge={systemStatusBadge}
        detectSystemStatusBadge={detectSystemStatusBadge}
        controlSystemStatusBadge={controlSystemStatusBadge}
      ></FirstRow>
      <SecondRow
        webSocketConnectionStatus={webSocketConnectionStatus}
        isDataReceived={isDataReceived}
        receivedData={receivedData}
        dispatch={dispatch}
      ></SecondRow>
      <ThirdRow></ThirdRow>
    </Container>
  );
};

export default DashBoard;
