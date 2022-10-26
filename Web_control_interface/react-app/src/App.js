import React, { useState } from "react";
import Navigation from "components/UI/nav/Navigation";
import SideBar from "components/UI/sidebar/SideBar";
import Divider from "components/UI/divider/Divider";
import DividerVertical from "components/UI/divider/Divider-vertical";
import Footer from "components/UI/footer/Footer";
import Main from "pages/main/Main"
import { IconContext, icons } from "components/UI/icon/icon-context";

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
