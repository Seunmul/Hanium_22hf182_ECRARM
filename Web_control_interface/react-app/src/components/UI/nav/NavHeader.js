import React from "react";

const NavHeader = ({ menuSelected }) => {
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
};

export default NavHeader;
