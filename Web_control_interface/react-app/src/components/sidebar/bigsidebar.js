import React, { useContext } from "react";
import { Nav } from "react-bootstrap";
import { IconContext } from "../icon/icon-context";

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
          menuSelectHandler(selectedKey);
        }}
      >
        {linkIcons}
      </Nav>
      <hr />
    </div>
  );
};

export default BigSideBar;
