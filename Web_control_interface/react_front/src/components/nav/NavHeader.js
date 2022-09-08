import React from "react";

const NavHeader = ({ menuSelected }) => {
    let header = ""
    switch (menuSelected) {
        case 0:
            header = "Home / Dashboard"
            break;
        case 1:
            header = "Detail information"
            break;
        case 2:
            header = "Control Panel"
            break;
        case 3:
            header = "Program Info"
            break;
        default:
            header = "error"
            break;
    }
    return (
        <span className="navigation-title">
            <a href="/#">
                <img
                    className=" d-flex d-sm-none"
                    src={process.env.PUBLIC_URL + '/img/ecrarm-logo.png'}
                    alt="main logo" width="42" height="42" />
            </a>
            <div className="d-none d-sm-block " style={{ fontSize: "1.1rem" }}>{header}</div>
        </span>
    );
};

export default NavHeader;
