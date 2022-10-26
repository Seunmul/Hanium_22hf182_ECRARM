import React from "react";

import styles from "stylesheets/Btn.module.css";


const Btn_si_mj = ({ children, className,style }) => {
  return (
    <div className={`${styles["btn-si-mj-320"]} ${className}`} style={style}>{children}</div>
  );
};

export default Btn_si_mj;
