import React from 'react'
import './icon-context.css'

const icons = [
    {
        logo: <i className="bi bi-house-door icon-context-size" />,
<<<<<<< HEAD:Web_control_interface/react_front/src/components/icon/icon-context.js
        name: "Home / Dashboard",
    },
    {
        logo: <i className="bi bi-table icon-context-size   " />,
        name: "Detail Information",
    },
    {
        logo: <i className="bi bi-person-workspace icon-context-size" />,
        name: "Control Panel",
    },
    {
        logo: <i className="bi bi-info-square icon-context-size " />,
        name: "Program Info",
=======
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
>>>>>>> 05cbcfc3e945d540d29636e0c36304db1441d59e:Web_control_interface/react-app/src/components/icon/icon-context.js
    },
]

const IconContext = React.createContext(icons)
export { icons,IconContext }
