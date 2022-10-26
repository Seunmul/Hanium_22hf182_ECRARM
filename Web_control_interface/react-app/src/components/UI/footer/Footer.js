import React from "react";
import styles from "stylesheets/Footer.module.css";

const Footer = () => {
  return (
    <div className={styles["footer-verti-layout"]}>
      <div className={styles["footer-layer1"]}>
        <div
          className="col-md-8 col-sm-12 d-flex flex-column align-items-flex-start px-3 "
          style={{ fontSize: "15px" }}
        >
          <strong style={{ fontSize: "21px" }}>ECRARM</strong>
          Element Classification Robot Arm
          <hr />
          <p className="text-muted" style={{ fontSize: "12px" }}>
            2022 한이음 ICT공모전 / 22HF_182
            <br />
            © 김영희.박건하.이희원.차우석 all right reserved
            <br />
            <br />
            <strong style={{ fontSize: "14px" }}>Developed by GeonhaPark.</strong>
          </p>
        </div>
        <div className={`col-md-4 ${styles["footer-layer1-icons"]}`}>
          <div>
            <i className={`bi-instagram ${styles["footer-icon-size"]}`}></i>
            <i className={`bi-facebook ${styles["footer-icon-size"]}`}></i>
            <i className={`bi-twitter  ${styles["footer-icon-size"]}`}></i>
          </div>
          <div className={styles["footer-layer1-used"]}>
            <a href="https://www.flaticon.com/kr/free-icons/-">
              - 아이콘 제작자: Freepik - Flaticon
            </a>
            <a href="https://www.fontspace.com/category/design">
              - title design : fontspace
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Footer;
