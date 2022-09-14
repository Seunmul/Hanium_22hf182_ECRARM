import React, { useState } from "react";
import Navigation from "./components/nav/Navigation";
import SideBar from "./components/sidebar/SideBar";
import Divider from "./components/divider/Divider";
import DividerVertical from "./components/divider/Divider-vertical";
import Footer from "./components/footer/Footer";
import Main from "./components/main/Main";
import { IconContext, icons } from "./components/icon/icon-context";

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

  const AppProps = {
    menuSelected,
    menuSelectHandler,
    sideBar,
    sideBarHandler,
  };

  return (
    <IconContext.Provider value={icons}>
      <div className="App">
        <SideBar {...AppProps} />
        <Divider />
        <div className="App-main-vertical">
          <Navigation {...AppProps} />
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
