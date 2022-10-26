import React from "react";
import { Accordion, Button, Col, Row, InputGroup } from "react-bootstrap";
import {
  connectionHandler,
  updateSendingMessage,
  setIsDataReceived,
} from "components/Util/reducer/websocketReducer";

const _second_row = ({
  webSocketConnectionStatus,
  isDataReceived,
  receivedData,
  dispatch
}) => {
  // 시작버튼 이벤트 핸들러
  const startButtonHandler = async () => {
    if (webSocketConnectionStatus === 1 && isDataReceived) {
      console.log("\n----start button clicked----");
      dispatch(setIsDataReceived(false));
      dispatch(updateSendingMessage("start"));
    }
  };
  // 멈춤버튼 이벤트 핸들러
  const stopButtonHandler = async () => {
    if (webSocketConnectionStatus === 1 && isDataReceived) {
      console.log("\n----stop button clicked----");
      dispatch(setIsDataReceived(false));
      dispatch(updateSendingMessage("stop"));
    }
  };
  // 매뉴얼버튼 이벤트 핸들러
  const manualButtonHandler = async () => {
    if (
      webSocketConnectionStatus === 1 &&
      isDataReceived &&
      receivedData.status === "waiting"
    ) {
      console.log("\n----manual mode in----");
      dispatch(setIsDataReceived(false));
      dispatch(updateSendingMessage("manual"));
    } else if (
      webSocketConnectionStatus === 1 &&
      isDataReceived &&
      receivedData.status === "manual"
    ) {
      console.log("\n----manual mode out----");
      dispatch(setIsDataReceived(false));
      dispatch(updateSendingMessage("waiting"));
    }
  };

  //매뉴얼 데이터 보내는 이벤트 핸들러
  const manualSendHandler = () => {
    dispatch(setIsDataReceived(false));
    dispatch(
      updateSendingMessage(
        JSON.stringify({
          X_Axis: 100,
          Y_Axis: 100,
          Z_Axis: 100,
          W_Axis: 100,
          R_Axis: 100,
        })
      )
    );
  };

  // 소켓 열기 버튼 이벤트 핸들러
  const openSocketHandler = () => {
    dispatch(connectionHandler("open"));
  };
  // 소켓 닫기 버튼 이벤트 핸들러
  const closeSocketHandler = () => {
    dispatch(connectionHandler("close"));
  };
  return (
    <Row
      id="2nd-row"
      style={{
        minHeight: "390px",
      }}
    >
      <Col style={{ margin: "10px 0px" }}>
        <Accordion
          defaultActiveKey={["0", "1"]}
          alwaysOpen
          style={{
            minWidth: "335px",
          }}
        >
          <Accordion.Item eventKey="0">
            <Accordion.Header>
              <h5>Quick Control Buttons</h5>
            </Accordion.Header>
            <Accordion.Body className="dash-button-area">
              <div className="dash-buttons">
                <Button
                  className={`mx-2 dash-button `}
                  variant={`${
                    receivedData.status === "waiting" &&
                    receivedData.status !== "initializing"
                      ? "success"
                      : "outline-success disabled"
                  }`}
                  onClick={startButtonHandler}
                >
                  Start Classification
                </Button>
                <Button
                  className={`mx-2 dash-button`}
                  variant={`${
                    receivedData.status !== "waiting" &&
                    receivedData.status !== "initializing"
                      ? receivedData.status !== "manual"
                        ? "danger"
                        : "outline-danger disabled"
                      : "outline-danger disabled"
                  }`}
                  onClick={stopButtonHandler}
                >
                  Stop
                </Button>
                <Button
                  className={`mx-2 dash-button`}
                  variant={`${
                    receivedData.status === "waiting" ||
                    receivedData.status === "manual"
                      ? "warning"
                      : "outline-warning disabled"
                  }`}
                  onClick={manualButtonHandler}
                >
                  {receivedData.status === "waiting"
                    ? "Manual Mode 시작"
                    : "Manual Mode 해제 "}
                </Button>
              </div>
            </Accordion.Body>
          </Accordion.Item>

          {receivedData.status === "manual" && (
            <Accordion.Item eventKey="1">
              <Accordion.Header>
                <h5>Manual Control Pannel</h5>
              </Accordion.Header>
              <Accordion.Body className="dash-control-panel-area">
                <InputGroup>
                  <InputGroup.Text>
                    X_AXIS : <input type="text"></input>
                  </InputGroup.Text>
                </InputGroup>
                <Button onClick={manualSendHandler}>Send Data</Button>
              </Accordion.Body>
            </Accordion.Item>
          )}

          <Accordion.Item eventKey="2">
            <Accordion.Header>
              <h5>Socket Connection Control</h5>
            </Accordion.Header>
            <Accordion.Body className="dash-button-area">
              <div className="dash-buttons">
                <Button
                  className="mx-2 dash-button"
                  variant="outline-primary "
                  onClick={openSocketHandler}
                >
                  Open Socket
                </Button>
                <Button
                  className="mx-2 dash-button"
                  variant="outline-dark"
                  onClick={closeSocketHandler}
                >
                  Close Socket
                </Button>
              </div>
            </Accordion.Body>
          </Accordion.Item>
        </Accordion>
      </Col>
      <Col style={{ margin: "10px 0px" }}>
        <Accordion
          defaultActiveKey={["0", "1"]}
          alwaysOpen
          style={{
            minWidth: "335px",
          }}
        >
          <Accordion.Item eventKey="0">
            <Accordion.Header>
              <h5>Detection Data</h5>
            </Accordion.Header>
            <Accordion.Body style={{ fontSize: "1.15rem", fontWeight: "450" }}>
              <div>
                Detected Class :{" "}
                {JSON.stringify(receivedData.Detector.data.class)}{" "}
              </div>
              <div>
                Element Accord_X :{" "}
                {JSON.stringify(receivedData.Detector.data.x)}
              </div>
              <div>
                Element Accord_Y :{" "}
                {JSON.stringify(receivedData.Detector.data.y)}
              </div>
            </Accordion.Body>
          </Accordion.Item>
          <Accordion.Item eventKey="1">
            <Accordion.Header>
              <h5>Axis Data</h5>
            </Accordion.Header>
            <Accordion.Body style={{ fontSize: "1.15rem", fontWeight: "450" }}>
              <div>
                X_Axis:{JSON.stringify(receivedData.Controller.data.X_Axis)}
              </div>
              <div>
                Y_Axis:{JSON.stringify(receivedData.Controller.data.Y_Axis)}
              </div>
              <div>
                Z_Axis:{JSON.stringify(receivedData.Controller.data.Z_Axis)}
              </div>
              <div>
                W_Axis:{JSON.stringify(receivedData.Controller.data.W_Axis)}
              </div>
              <div>
                R_Axis:{JSON.stringify(receivedData.Controller.data.R_Axis)}
              </div>
            </Accordion.Body>
          </Accordion.Item>
        </Accordion>
      </Col>

      <Col style={{ margin: "10px 0px" }}>
        <Accordion
          defaultActiveKey={["0"]}
          alwaysOpen
          style={{
            minWidth: "335px",
          }}
        >
          <Accordion.Item eventKey="0">
            <Accordion.Header>
              <h5>Full Current Data</h5>
            </Accordion.Header>
            <Accordion.Body style={{ fontSize: "1rem", fontWeight: "450" }}>
              {JSON.stringify(receivedData, null, 10)}
            </Accordion.Body>
          </Accordion.Item>
        </Accordion>
      </Col>
    </Row>
  );
};

export default _second_row;
