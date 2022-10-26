import React from "react";
import "stylesheets/icon-context.css";

const icons = [
  {
    logo: <i className="bi bi-house-door icon-context-size" />,
    name: "DASHBOARD",
  },
  {
    logo: <i className="bi bi-table icon-context-size   " />,
    name: "DETAIL STATUS",
  },
  {
    logo: <i className="bi bi-person-workspace icon-context-size" />,
    name: "CONTROL PANEL",
  },
  {
    logo: <i className="bi bi-info-square icon-context-size " />,
    name: "PROGRAM INFO",
  },
];

const IconContext = React.createContext(icons);

export { icons, IconContext };
