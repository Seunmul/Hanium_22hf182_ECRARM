import { Navbar } from "react-bootstrap";
import SmallSideBar from "./smallsidebar";
import BigSideBar from "./bigsidebar";
import "./SideBar.css";

<<<<<<< HEAD:Web_control_interface/react_front/src/components/sidebar/SideBar.js
const SideBar = ({ menuSelected, onMenuSelect, sideBar, sideBarHandler }) => {
  const sidebar = sideBar ? (
    <SmallSideBar menuSelected={menuSelected} onMenuSelect={onMenuSelect} />
  ) : (
    <BigSideBar menuSelected={menuSelected} onMenuSelect={onMenuSelect} />
=======
const SideBar = ({ menuSelected, menuSelectHandler, sideBar, sideBarHandler }) => {
  const sidebar = sideBar ? (
    <SmallSideBar menuSelected={menuSelected} menuSelectHandler={menuSelectHandler} />
  ) : (
    <BigSideBar menuSelected={menuSelected} menuSelectHandler={menuSelectHandler} />
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/sidebar/SideBar.js
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
<<<<<<< HEAD:Web_control_interface/react_front/src/components/sidebar/SideBar.js

=======
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/sidebar/SideBar.js
          ></i>
        ) : (
          <i
            className="bi bi-chevron-left "
            style={{ fontSize: "25px" }}

          ></i>
        )}
      </div>
<<<<<<< HEAD:Web_control_interface/react_front/src/components/sidebar/SideBar.js

=======
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/sidebar/SideBar.js
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
<<<<<<< HEAD:Web_control_interface/react_front/src/components/sidebar/SideBar.js
            padding: "12px 0px 0px 0px",
          }}
        >
          <Navbar.Brand href="/#"
=======
            padding: "12px 0px 12px 0px",
          }}
        >
          <Navbar.Brand href="/App#"
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/sidebar/SideBar.js
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
