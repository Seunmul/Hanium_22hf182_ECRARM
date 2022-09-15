import React, { useContext } from "react";
import { Nav } from "react-bootstrap";
import { IconContext } from "../icon/icon-context";

<<<<<<< HEAD:Web_control_interface/react_front/src/components/sidebar/smallsidebar.js
const SmallSideBar = ({ menuSelected, onMenuSelect }) => {
  const icons = useContext(IconContext)
  const linkIcons = icons.map((icon, i) => {
    return (
      <Nav.Item key={i} className="" as="li">
        <Nav.Link
          style={{ display: "flex" }}
          className={`small-sidebar-icon text-white ${menuSelected === i && "active"
            }`}
          href={`/#`}
=======
const SmallSideBar = ({ menuSelected, menuSelectHandler }) => {
  const icons = useContext(IconContext);
  const linkIcons = icons.map((icon, i) => {
    return (
      <Nav.Item key={i} className="sidebar-item sidebar-item:hover" as="li">
        <Nav.Link
          style={{ display: "flex" }}
          className={`small-sidebar-icon text-white `}
          id={`${menuSelected === i && "menu-active"}`}
          href={`/App#`}
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/sidebar/smallsidebar.js
          eventKey={`${i}`}
        >
          {icon.logo}
        </Nav.Link>
      </Nav.Item>
    );
  });
  return (
    <div className="small-sidebar">
      <hr />
      <Nav
        variant="pills"
        className="flex-column justify-items-center text-center mb-auto small-sidebar"
        defaultActiveKey="/"
        as="ul"
        onSelect={(selectedKey) => {
<<<<<<< HEAD:Web_control_interface/react_front/src/components/sidebar/smallsidebar.js
          onMenuSelect(selectedKey);
=======
          menuSelectHandler(selectedKey);
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/sidebar/smallsidebar.js
        }}
      >
        {linkIcons}
      </Nav>
      <hr />
<<<<<<< HEAD:Web_control_interface/react_front/src/components/sidebar/smallsidebar.js

=======
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/sidebar/smallsidebar.js
    </div>
  );
};

export default SmallSideBar;
