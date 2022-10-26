import React from "react";
import { ProgressBar} from "react-bootstrap";

const ControlPanel = ({ style }) => {
  return (
    <div style={style}>
      <div
        className="div-fluid"
        style={{
          paddingLeft: "0px",
          paddingRight: "0px",
        }}
      >
        <div className="table-layout">
          <div className="table-cell fixed-width-cell">
            <h3>Control Manipulator</h3>
            In Progress:
            <ProgressBar animated now={60} label={`${60}%`} />
            <br />
            <div id="mPosition" style={{ display: "none" }}>
              <center>
                <div
                  id="mX"
                  style={{
                    textAlign: "left",
                    paddingLeft: "15px",
                    margin: "4px",
                    fontSize: "30px",
                    width: "190px",
                    border: "1px solid #aaa",
                    fontWeight: "bold",
                  }}
                >
                  X: 0.000
                </div>
                <div
                  id="mY"
                  style={{
                    textAlign: "left",
                    paddingLeft: "15px",
                    margin: "4px",
                    fontSize: "30px",
                    width: "190px",
                    border: "1px solid #aaa",
                    fontWeight: "bold",
                  }}
                >
                  Y: 0.000
                </div>
                <div
                  id="mZ"
                  style={{
                    textAlign: "left",
                    paddingLeft: "15px",
                    margin: "4px",
                    fontSize: "30px",
                    width: "190px",
                    border: "1px solid #aaa",
                    fontWeight: "bold",
                  }}
                >
                  Z: 0.000
                </div>
              </center>
            </div>
            <div id="wPosition">
              <center>
                <div
                  id="wX"
                  style={{
                    textAlign: "left",
                    paddingLeft: "15px",
                    margin: "4px",
                    fontSize: "30px",
                    width: "190px",
                    border: "1px solid #aaa",
                    fontWeight: "bold",
                  }}
                >
                  X: 0.000
                </div>
                <div
                  id="wY"
                  style={{
                    textAlign: "left",
                    paddingLeft: "15px",
                    margin: "4px",
                    fontSize: "30px",
                    width: "190px",
                    border: "1px solid #aaa",
                    fontWeight: "bold",
                  }}
                >
                  Y: 0.000
                </div>
                <div
                  id="wZ"
                  style={{
                    textAlign: "left",
                    paddingLeft: "15px",
                    margin: "4px",
                    fontSize: "30px",
                    width: "190px",
                    border: "1px solid #aaa",
                    fontWeight: "bold",
                  }}
                >
                  Z: 0.000
                </div>
              </center>
            </div>
            <center>
              <div
                className="input-group"
                style={{ clear: "both", width: "250px" }}
              >
                <span className="input-group-btn">
                  <button
                    type="button"
                    className="btn btn-sm btn-primary"
                    id="sendReset"
                  >
                    RESET
                  </button>
                  <button
                    type="button"
                    className="btn btn-sm btn-primary"
                    id="sendUnlock"
                  >
                    UNLOCK
                  </button>
                  <button
                    type="button"
                    className="btn btn-sm btn-primary"
                    id="sendHome"
                  >
                    HOME
                  </button>
                  <button
                    type="button"
                    className="btn btn-primary"
                    style={{ marginTop: "5px" }}
                    id="sendZero"
                  >
                    Zero Machine (G92)
                  </button>
                </span>
              </div>
            </center>
            <hr style={{ clear: "both" }} />
            <select className="form-control" id="jogSpeed">
              <option value="1500">Feed Rate: 1500</option>
              <option value="1000">Feed Rate: 1000</option>
              <option defaultValue={"500"}>Feed Rate: 500</option>
              <option value="100">Feed Rate: 100</option>
              <option value="5">Feed Rate: 5</option>
            </select>
            <select className="form-control" id="jogSize">
              <option value=".5">Distance: .5</option>
              <option defaultValue={"1"}>Distance: 1</option>
              <option value="2">Distance: 2</option>
              <option value="5">Distance: 5</option>
              <option value="10">Distance: 10</option>
              <option value="20">Distance: 20</option>
            </select>
            <br style={{ clear: "both" }} />
            <center>
              <div>
                <div blk="" id="yP" className="btn btn-primary">
                  +X
                </div>
                <div blk="" id="zP" className="btn btn-primary">
                  +Y
                </div>
                <div blk="" id="xM" className="btn btn-primary">
                  +Z
                </div>

                <div blk="" id="xP" className="btn btn-primary">
                  -X
                </div>
                <div blk="" id="yM" className="btn btn-primary">
                  -Y
                </div>
                <div blk="" id="zM" className="btn btn-primary">
                  -Z
                </div>
              </div>
            </center>
            <br style={{ clear: "both" }} />
            <center>
              <div>
                <div blk="" id="spnCW" className="btn btn-primary">
                  CW
                </div>
                <div blk="" id="spnCCW" className="btn btn-primary">
                  CCW
                </div>
                <div blk="" id="spn" className="btn btn-primary">
                  Spindle
                </div>
                <div blk="" id="cool" className="btn btn-primary">
                  Coolant
                </div>
              </div>
            </center>
            <br style={{ clear: "both" }} />
            <center>
              <div>
                <div h2="" id="stopStart" className="btn btn-info">
                  Stop/Start
                </div>
                <div h2="" id="abort" className="btn btn-danger">
                  Abort
                </div>
              </div>
            </center>
            <hr style={{ clear: "both" }} />
            <span style={{ color: "#aaa", fontSize: ".8em" }} />
            <span style={{ color: "red" }}>axis step hotkeys:</span>
            WASD, up/down-arrow
          </div>
        </div>
        <div className="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main" />

        <div style={{ clear: "both", float: "right", marginTop: "10px" }} />
      </div>
    </div>
  );
};

export default ControlPanel;
