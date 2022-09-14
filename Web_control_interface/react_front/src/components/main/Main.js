import Home from "./Home";
import Detail from "./Detail";
import Information from "./Information";
import ControlPanel from "./ControlPanel";
import WebSocketComponent from "../../websocket/websocket";

const Main = ({ menuSelected }) => {
  const style = {
    display: "flex",
    flexDirection: "column",
    alignContent:"center",
    width: "100%",
    height: "100%",
    marginTop: "10px",
    padding: "15px",
    fontFamily:"Noto Sans"
  };
  let main = <div></div>
  switch (menuSelected) {
    case 0:
      main = <Home style={style} />;
      break;
    case 1:
      main = <Detail style={style} />;
      break;
    case 2:
      main = <ControlPanel style={style} />;
      break;
    case 3:
      main = <Information style={style} />;
      break;
    default:
      main = <div>"No DATA"</div>;
      break;
  }
  return <>
    {main}
    <WebSocketComponent></WebSocketComponent>
  </>
};

export default Main