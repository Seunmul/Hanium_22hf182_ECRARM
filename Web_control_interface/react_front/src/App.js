import React, { useState } from "react";
import Navigation from "./components/nav/Navigation";
import SideBar from "./components/sidebar/SideBar";
import Divider from "./components/divider/Divider";
import DividerVertical from "./components/divider/Divider-vertical";
import Footer from "./components/footer/Footer";
import Main from "./components/main/Main";
import { IconContext, icons } from "./components/icon/icon-context"

import "./App.css";

function App() {
  const [menuSelected, setMenuSelected] = useState(+0);
  const [sideBar, setSideBarSmall] = useState(true);

  const menuSelectHandler = (menuNumber) => {
    setMenuSelected((prevMenuNumber) => +menuNumber);
  };
  const sideBarHandler = () => {
    setSideBarSmall((sideBar) => !sideBar);
  };

  return (
    <IconContext.Provider value={icons}>
      <div className="App">
        <SideBar
          menuSelected={menuSelected}
          onMenuSelect={menuSelectHandler}
          sideBar={sideBar}
          sideBarHandler={sideBarHandler}
        />
        <Divider />
        <div className="App-main-vertical">
          <Navigation
            menuSelected={menuSelected}
            onMenuSelect={menuSelectHandler}
            sideBar={sideBar}
            sideBarHandler={sideBarHandler}
          // style={{ width: "100%" }}
          />
          <Main menuSelected={menuSelected} />
          <Footer />
          <DividerVertical />
        </div>
        <Divider />
      </div>

    </IconContext.Provider>
  );
}

export default App;


