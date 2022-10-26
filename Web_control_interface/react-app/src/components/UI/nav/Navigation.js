import React, { useContext } from "react";
import { Container, Nav, Navbar } from "react-bootstrap";
import { IconContext } from "../icon/icon-context";
import LoginLogo from "../icon/loginlogo";
import LoginLogoLight from "../icon/loginlogo-light";
import NavHeader from "./NavHeader";
import "stylesheets/Navigation.css";

const Navigation = ({
  menuSelected,
  menuSelectHandler,
  sideBar,
  sideBarHandler,
}) => {
  const icons = useContext(IconContext);
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
        </Container>
      </Nav>
    </>
  );
};

export default Navigation;

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
