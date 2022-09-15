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
<<<<<<< HEAD:Web_control_interface/react_front/src/components/main/Main.js
    padding: "30px",
=======
    padding: "15px",
    fontFamily:"Noto Sans"
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/main/Main.js
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