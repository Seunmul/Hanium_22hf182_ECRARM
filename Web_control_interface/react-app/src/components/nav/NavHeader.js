import React from "react";

const NavHeader = ({ menuSelected }) => {
<<<<<<< HEAD:Web_control_interface/react_front/src/components/nav/NavHeader.js
    let header = ""
    switch (menuSelected) {
        case 0:
            header = "Home / Dashboard"
            break;
        case 1:
            header = "Detail information"
            break;
        case 2:
            header = "Control Panel"
            break;
        case 3:
            header = "Program Info"
            break;
        default:
            header = "error"
            break;
    }
    return (
        <span className="navigation-title">
            <a href="/#">
                <img
                    className=" d-flex d-sm-none"
                    src={process.env.PUBLIC_URL + '/img/ecrarm-logo.png'}
                    alt="main logo" width="42" height="42" />
            </a>
            <div className="d-none d-sm-block " style={{ fontSize: "1.1rem" }}>{header}</div>
        </span>
    );
=======
  let header = "";
  switch (menuSelected) {
    case 0:
      header = "DASHBOARD";
      break;
    case 1:
      header = "DETAIL STATUS";
      break;
    case 2:
      header = "CONTROL PANEL";
      break;
    case 3:
      header = "PROGRAM INFO";
      break;
    default:
      header = "NO PAGE";
      break;
  }
  return (
    <span className="navigation-title">
      <a href="/App#" style={{ fontSize: "1.3rem",color:"black",fontStyle:"normal",textDecorationLine:"none" }}>
        <img
          className=" d-flex d-sm-none"
          src={process.env.PUBLIC_URL + "/img/ecrarm-logo.png"}
          alt="main logo"
          width="42"
          height="42"
        />
        {/* <img
          src={process.env.PUBLIC_URL + "/img/ecrarm-title3.png"}
          alt="main logo"
          width="145"
          height="27"
          className="mx-3 my-3 d-sm-none"
        /> */}

        <div className="d-none d-sm-block " >
          {header}
        </div>
      </a>
    </span>
  );
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/nav/NavHeader.js
};

export default NavHeader;
