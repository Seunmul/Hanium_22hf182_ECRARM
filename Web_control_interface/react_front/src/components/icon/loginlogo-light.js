import React from "react";
import pica from "../img/pica.jpg"

const LoginLogo = () => {
  return (
    <div
      className="dropdown"
      id="navigation-user"
      style={{ flexDirection: "column", height: "35px" }}
    >
      <div
        className="d-flex align-items-center justify-content-center text-center p-3 link-light text-decoration dropdown-toggle"
        id="dropdownUser3"
        data-bs-toggle="dropdown"
        aria-expanded="false"
        style={{ height: "32px" }}
      >
        <img
          src={pica}
          alt="picachu logo"
          width="38"
          height="38"
          className="rounded-circle me-2 "
        />
      </div>
      <ul className="dropdown-menu text-small" aria-labelledby="dropdownUser3">
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
  );
};

export default LoginLogo;
