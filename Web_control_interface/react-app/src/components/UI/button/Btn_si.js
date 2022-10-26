import React from "react";
import styles from "stylesheets/Btn.module.css";

const Btn_si = ({ loginBy, imgSrc }) => {
  return (
    <div className={styles["btn-si"]} id={styles["btn-si-gg"]}>
      <div id={styles["login-icon-size"]}>
        <img className={styles["login-icon"]} src={imgSrc}></img>
      </div>
      <div>{loginBy}</div>
      <div id={styles["login-icon-size"]}></div>
    </div>
  );
};

export default Btn_si;
