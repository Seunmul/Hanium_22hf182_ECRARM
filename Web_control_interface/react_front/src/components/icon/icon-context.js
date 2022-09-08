import React from 'react'
import './icon-context.css'

const icons = [
    {
        logo: <i className="bi bi-house-door icon-context-size" />,
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
    },
]

const IconContext = React.createContext(icons)
export { icons,IconContext }
