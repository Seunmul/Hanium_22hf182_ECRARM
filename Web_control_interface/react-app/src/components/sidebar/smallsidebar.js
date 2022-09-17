import React, { useContext } from "react";
import { Nav } from "react-bootstrap";
import { IconContext } from "../icon/icon-context";

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
          menuSelectHandler(selectedKey);
        }}
      >
        {linkIcons}
      </Nav>
      <hr />
    </div>
  );
};

export default SmallSideBar;
