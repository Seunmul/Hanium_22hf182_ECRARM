import React, { useContext } from "react";
import { Nav } from "react-bootstrap";
import { IconContext } from "../icon/icon-context";

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
          onMenuSelect(selectedKey);
        }}
      >
        {linkIcons}
      </Nav>
      <hr />
    </div>
  );
};

export default BigSideBar;
