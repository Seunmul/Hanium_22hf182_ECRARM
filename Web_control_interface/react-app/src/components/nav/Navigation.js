import React, { useContext } from "react";
import { Container, Nav, Navbar } from "react-bootstrap";
import { IconContext } from "../icon/icon-context";
import LoginLogo from "../icon/loginlogo";
<<<<<<< HEAD:Web_control_interface/react_front/src/components/nav/Navigation.js
=======
import LoginLogoLight from "../icon/loginlogo-light";
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/nav/Navigation.js
import NavHeader from "./NavHeader";
import "./Navigation.css";

const Navigation = ({
  menuSelected,
<<<<<<< HEAD:Web_control_interface/react_front/src/components/nav/Navigation.js
  onMenuSelect,
=======
  menuSelectHandler,
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/nav/Navigation.js
  sideBar,
  sideBarHandler,
}) => {
  const icons = useContext(IconContext);
<<<<<<< HEAD:Web_control_interface/react_front/src/components/nav/Navigation.js
  const linkIcons = icons.map((icon, i) => {
    return (
      <Nav.Item
        key={i}
        data-bs-toggle="collapse"
        data-bs-target="#navbarsExample03"
        as="li"
      >
        <Nav.Link
          aria-current="page"
          style={{ display: "flex", fontWeight: "400" }}
          className={`navigation-icon text-black ${
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
  const toggleMenu = (
    <Nav
      className="me-auto mb-2 mb-sm-0 flex-column flex-column container"
      defaultActiveKey="/"
      as="ul"
      onSelect={(selectedKey) => {
        onMenuSelect(selectedKey);
      }}
    >
      <Nav.Item
        data-bs-toggle="collapse"
        data-bs-target="#navbarsExample03"
        as="li"
      >
        <hr />
        <div
          className="my-4"
          style={{
            display: "flex",
            justifyContent: "center",
            alignContent: "center",
            fontWeight: "400",
            textAlign: "center",
          }}
        >
          <img
            src={process.env.PUBLIC_URL + "/img/ecrarm-title3.png"}
            alt="main logo"
            width="145"
            height="27"
            className="mx-3"
          />
        </div>
      </Nav.Item>
      {linkIcons}
        <hr />
    </Nav>
  );

  return (
    <>
      <Nav
        className="navbar sticky-top navbar-light bg-light"
        aria-label="Third navbar example"
        style={{ width: "100%" }}
      >
        <Container fluid style={{ padding: "3px", margin: "0px 1.5rem" }}>
          <Navbar.Toggle
            className="d-flex d-sm-none "
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarsExample03"
            aria-controls="navbarsExample03"
            aria-expanded="false"
            aria-label="Toggle navigation"
            style={{ border: "0px" }}
            onClick={sideBarHandler}
          >
            <i className="bi bi-list" style={{ fontSize: "23px" }} />
          </Navbar.Toggle>
          <NavHeader menuSelected={menuSelected} />
          <LoginLogo />
          <Navbar.Collapse id="navbarsExample03" className="d-sm-none">
            {toggleMenu}
          </Navbar.Collapse>
=======
  const toggleMenu = (
    <Nav
      className="flex-column"
      onSelect={(selectedKey) => {
        menuSelectHandler(selectedKey);
      }}
    >
      <div style={{ marginTop: "10px" }}></div>
      {icons.map((icon, i) => {
        return (
          <Nav.Item
            className={`navigation-item navigation-item:hover my-1
            ${menuSelected === i && "navigation-item-current"}`}
            key={i}
            data-bs-toggle="collapse"
            data-bs-target="#navbarToggleMenu"
          >
            <Nav.Link id={`navigation-icon`} href={`/App#`} eventKey={`${i}`}>
              {icon.logo}
              <div className="mx-2">{icon.name}</div>
            </Nav.Link>
          </Nav.Item>
        );
      })}
    </Nav>
  );
  return (
    <>
      <Nav
        className="navbar sticky-top bg-light d-none d-sm-flex"
        style={{ minHeight: "80px", width: "100%" }}
      >
        <Container
          fluid
          style={{ padding: "11px", margin: "0px 1.5rem", height: "100%" }}
        >
          <NavHeader menuSelected={menuSelected} />
          <LoginLogo />
        </Container>
      </Nav>
      <Nav
        className="navbar sticky-top d-sm-none "
        style={{ minHeight: "80px", width: "100%", backgroundColor: "#353535" }}
      >
        <Container
          fluid
          style={{ padding: "11px", margin: "0px 1.5rem", height: "100%" }}
        >
          <Navbar.Toggle
            className="d-flex"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarToggleMenu"
            style={{ border: "0px" }}
            onClick={sideBarHandler}
          >
            <i
              className="bi bi-list"
              style={{ fontSize: "23px", color: "white" }}
            />
          </Navbar.Toggle>
          <NavHeader menuSelected={menuSelected} />
          <LoginLogoLight />
          <Navbar.Collapse id="navbarToggleMenu">{toggleMenu}</Navbar.Collapse>
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/nav/Navigation.js
        </Container>
      </Nav>
    </>
  );
};

export default Navigation;
<<<<<<< HEAD:Web_control_interface/react_front/src/components/nav/Navigation.js
=======

//  {/* <Nav.Item
//         data-bs-toggle="collapse"
//         data-bs-target="#navbarsExample03"
//         as="li"
//       >
//         <div
//           className="my-4"
//           style={{
//             display: "flex",
//             justifyContent: "center",
//             alignContent: "center",
//             fontWeight: "400",
//             textAlign: "center",
//           }}
//         >
//           <img
//             src={process.env.PUBLIC_URL + "/img/ecrarm-title3.png"}
//             alt="main logo"
//             width="145"
//             height="27"
//             className="mx-3"
//           />
//         </div>
//       </Nav.Item> */}
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/nav/Navigation.js
