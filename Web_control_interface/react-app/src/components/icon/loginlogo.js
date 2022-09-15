import React from "react";
<<<<<<< HEAD:Web_control_interface/react_front/src/components/icon/loginlogo.js

const LoginLogo = () => {
  return (
    <div
      className="dropdown"
      id="navigation-user"
      style={{ flexDirection: "column", height: "35px" }}
    >
      <div
        className="d-flex align-items-center justify-content-center text-center link-dark text-decoration dropdown-toggle"
        id="dropdownUser3"
        data-bs-toggle="dropdown"
        aria-expanded="false"
        style={{ height: "32px" }}
      >
        <img
          src={process.env.PUBLIC_URL+'/img/pica.jpg'}
=======
import { Dropdown } from "react-bootstrap";

const LoginLogo = () => {
  return (
    <Dropdown
      id="navigation-user"
      style={{ flexDirection: "column", height: "35px" }}
    >
      <Dropdown.Toggle
        variant="light"
        className="d-flex align-items-center justify-content-center text-center link-dark text-decoration"
        style={{ height: "42px", witdh: "56px" }}
      >
        <img
          src={process.env.PUBLIC_URL + "/img/pica.jpg"}
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/icon/loginlogo.js
          alt="picachu logo"
          width="38"
          height="38"
          className="rounded-circle"
        />
<<<<<<< HEAD:Web_control_interface/react_front/src/components/icon/loginlogo.js
      </div>
      <ul className="dropdown-menu" style={{textSize:"15px"}} aria-labelledby="dropdownUser3">
        <li>
          <div className="dropdown-item">New project...</div>
        </li>
        <li>
          <div className="dropdown-item">Settings</div>
        </li>
        <li>
          <div className="dropdown-item">Profile</div>
        </li>
        <li>
          <hr className="dropdown-divider" />
        </li>
        <li>
          <div className="dropdown-item">Sign out</div>
        </li>
      </ul>
    </div>
=======
      </Dropdown.Toggle>
      <Dropdown.Menu style={{ textSize: "15px" }}>
        <Dropdown.Header>User Menu</Dropdown.Header>
        <Dropdown.Item>New project...</Dropdown.Item>
        <Dropdown.Item>Settings</Dropdown.Item>
        <Dropdown.Item>Profile</Dropdown.Item>
        <Dropdown.Divider />
        <Dropdown.Item href="/">Sign out</Dropdown.Item>
      </Dropdown.Menu>
    </Dropdown>
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/icon/loginlogo.js
  );
};

export default LoginLogo;
