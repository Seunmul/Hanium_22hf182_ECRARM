import React from "react";

const LoginLogo = () => {
  return (
    <div
      className="dropdown"
      id="navigation-user"
      style={{ flexDirection: "column", height: "35px" }}
    >
      <div
        className="d-flex align-items-center justify-content-center text-center link-dark text-decoration dropdown-toggle"
        id="dropdownUser3"
        data-bs-toggle="dropdown"
        aria-expanded="false"
        style={{ height: "32px" }}
      >
        <img
          src={process.env.PUBLIC_URL+'/img/pica.jpg'}
          alt="picachu logo"
          width="38"
          height="38"
          className="rounded-circle"
        />
      </div>
      <ul className="dropdown-menu" style={{textSize:"15px"}} aria-labelledby="dropdownUser3">
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
