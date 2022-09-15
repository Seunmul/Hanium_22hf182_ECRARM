import React, { useContext } from "react";
import { Nav } from "react-bootstrap";
import { IconContext } from "../icon/icon-context";

<<<<<<< HEAD:Web_control_interface/react_front/src/components/sidebar/bigsidebar.js
const BigSideBar = ({ menuSelected, onMenuSelect }) => {
  const icons = useContext(IconContext)
  const linkIcons = icons.map((icon, i) => {
    return (
      <Nav.Item key={i} className="" as="li">
        <Nav.Link
          style={{ display: "flex" }}
          className={`sidebar-icon text-white ${
            menuSelected === i && "active"
          }`}
          href={`/#`}
          eventKey={`${i}`}
        >
          {icon.logo}
          <div className="mx-2">{icon.name}</div>
=======
const BigSideBar = ({ menuSelected, menuSelectHandler }) => {
  const icons = useContext(IconContext);
  const linkIcons = icons.map((icon, i) => {
    return (
      <Nav.Item key={i} className="sidebar-item sidebar-item:hover" as="li">
        <Nav.Link
          style={{ display: "flex" }}
          className={`sidebar-icon text-white `}
          id={`${menuSelected === i && "menu-active"}`}
          href={`/App#`}
          eventKey={`${i}`}
        >
          {icon.logo}
          <div className="mx-2" style={{fontSize:"1.1rem",fontWeight:"500"}}>{icon.name}</div>
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/sidebar/bigsidebar.js
        </Nav.Link>
      </Nav.Item>
    );
  });
  return (
    <div className="sidebar">
      <hr />
      <Nav
        variant="pills"
        className="flex-column flex-column mb-auto container"
        defaultActiveKey="/"
        as="ul"
        onSelect={(selectedKey) => {
<<<<<<< HEAD:Web_control_interface/react_front/src/components/sidebar/bigsidebar.js
          onMenuSelect(selectedKey);
=======
          menuSelectHandler(selectedKey);
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/sidebar/bigsidebar.js
        }}
      >
        {linkIcons}
      </Nav>
      <hr />
    </div>
  );
};

export default BigSideBar;
