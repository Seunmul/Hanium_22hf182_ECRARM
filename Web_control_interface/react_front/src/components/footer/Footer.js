import React from "react";

const Footer = ({ style }) => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "20%",
        width: "100%",
        padding: "30px",
      }}
    >
      <footer className="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
        <div
          className="col-md-4 d-flex flex-column align-items-flex-start px-3 "
          style={{ fontSize: "15px" }}
        >
          <strong style={{ fontSize: "21px" }}>ECRARM</strong>
          Element Classification Robot Arm
          <hr />
          <div className="d-flex text-muted" style={{ fontSize: "12px" }}>
            2022 Hanium ICT공모전 / 22hf_182 <br /> ©
            김영희.박건하.이희원.차우석 all right reserved
          </div>
          <br/>
          <a
            href="https://www.flaticon.com/kr/free-icons/-"
            title="- 아이콘"
            style={{ fontSize: "5px" }}
          >
            - 아이콘 제작자: Freepik - Flaticon
          </a>
          <a href="https://www.fontspace.com/category/design">
            - title design : fontspace
          </a>
        </div>
        <ul className="nav col-md-4 justify-content-end list-unstyled d-flex px-3">
          <li className="ms-3">
            <div className="text-muted">
              <i className="bi-instagram" style={iconSize}></i>
            </div>
          </li>
          <li className="ms-3">
            <div className="text-muted">
              <i className="bi-facebook" style={iconSize}></i>
            </div>
          </li>
          <li className="ms-3">
            <div className="text-muted">
              <i className="bi-twitter" style={iconSize}></i>
            </div>
          </li>
        </ul>
      </footer>
    </div>
  );
};

export default Footer;

const iconSize = { fontSize: 30 };
