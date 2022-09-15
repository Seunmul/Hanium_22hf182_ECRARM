import React from "react";
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
          alt="picachu logo"
          width="38"
          height="38"
          className="rounded-circle"
        />
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
  );
};

export default LoginLogo;
