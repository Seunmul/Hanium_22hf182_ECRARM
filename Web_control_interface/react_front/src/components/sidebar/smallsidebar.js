import React, { useContext } from "react";
import { Nav } from "react-bootstrap";
import { IconContext } from "../icon/icon-context";

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
          onMenuSelect(selectedKey);
        }}
      >
        {linkIcons}
      </Nav>
      <hr />

    </div>
  );
};

export default SmallSideBar;
