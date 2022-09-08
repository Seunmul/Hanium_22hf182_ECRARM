import { Navbar } from "react-bootstrap";
import SmallSideBar from "./smallsidebar";
import BigSideBar from "./bigsidebar";
import "./SideBar.css";

const SideBar = ({ menuSelected, onMenuSelect, sideBar, sideBarHandler }) => {
  const sidebar = sideBar ? (
    <SmallSideBar menuSelected={menuSelected} onMenuSelect={onMenuSelect} />
  ) : (
    <BigSideBar menuSelected={menuSelected} onMenuSelect={onMenuSelect} />
  );
  const toggleBtn = (
    <div
      style={{
        display: "flex",
        justifyContent: `${sideBar ? "center" : "flex-end"}`,
        alignContent: "center",
      }}
    >
      <div
        className="toggleBtn toggleBtn:hover"
        onClick={sideBarHandler}
      >
        {sideBar ? (
          <i
            className="bi bi-chevron-right "
            style={{ fontSize: "25px" }}

          ></i>
        ) : (
          <i
            className="bi bi-chevron-left "
            style={{ fontSize: "25px" }}

          ></i>
        )}
      </div>

    </div>
  );
  return (
    <div className="d-none d-sm-flex navbar-fluid flex-column flex-shrink-0 p-3 pt-0 text-white bg-dark">
      <div
        className="sticky-top pt-2"
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: `${sideBar ? "center" : "center"}`,
        }}
      >
        <Navbar
          bg="dark"
          variant="dark"
          style={{
            display: "flex",
            flexDirection: `${sideBar ? "column" : "row"}`,
            justifyContent: `${sideBar ? "center" : "center"}`,
            padding: "12px 0px 0px 0px",
          }}
        >
          <Navbar.Brand href="/#"
            style={{
              padding: "0px",
              margin: "0px"
            }}>
            <img src={process.env.PUBLIC_URL + '/img/ecrarm-logo.png'}
              alt="main logo" width="42" height="42" className="" />
            {!sideBar && (
              <img src={process.env.PUBLIC_URL + '/img/ecrarm-title3.png'}
                alt="main logo" width="135" height="25" className="mx-3" />
            )}
          </Navbar.Brand>

        </Navbar>
        {sidebar}
        {toggleBtn}
      </div>
    </div>
  );
};

export default SideBar;
