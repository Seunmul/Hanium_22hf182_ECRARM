import React from "react";
import styles from "./Input_si.module.css";


const Input_si = ({
  title,
  type,
  placeholder,
  children,
}) => {
  
  return (
    <>
      <div className={styles["input-si"]}>
        <div className={styles["input-si-title"]}>{title}</div>
        <input
          className={styles["input-si-box"]}
          type={type}
          placeholder={placeholder}
        ></input>
      </div>
      {children}
    </>
  );
};

export default Input_si;
