import React, { useState } from "react";
import { Link } from "react-router-dom";

import Btn from "components/UI/button/Btn_si_mj";
import Input from "components/UI/Input_si";
import ValidMsg from "components/UI/ValidMsg";
import styles from "stylesheets/SignIn.module.css";

const SignIn = () => {
  const [isValid, setIsValid] = useState(true);

  const validHandler = () => {
    setIsValid(!isValid);
  };

  return (
    <>
      <div className={styles["sign-in"]}>
        <div className={styles["sign-in-loginbox"]}>
          <div
            className={styles["sign-in-title"]}
            style={{ margin: "60px 0px 38px 0px" }}
          >
            <img
              src={process.env.PUBLIC_URL + "/img/ecrarm-title3.png"}
              width="250"
              height="50"
              alt="ecrarm-title"
            />
          </div>

          <Input title="아이디" type="text" placeholder="아이디를 입력하세요" />
          <Input
            title="비밀번호"
            type="password"
            placeholder="비밀번호를 입력하세요"
          >
            <ValidMsg check={isValid}>
              아이디 혹은 비밀번호를 확인해주세요.
            </ValidMsg>
          </Input>
          <Link to="/App" style={{ textDecorationLine: "none", color: "black" }}>
            <Btn style={{ marginTop: "24px" }} onClick={{ validHandler }}>
              로그인
            </Btn>
          </Link>

          <div className={styles["rq-msg"]}>
            <span style={{ marginRight: "3px" }}>
              관리자 계정이 없으시다면 ?
            </span>
            <Link to="/SignUp">
              <span style={{ color: "#4981F2" }}>회원가입</span>
            </Link>
          </div>
        </div>
      </div>
      <footer
        className="d-flex flex-wrap align-items-center py-3 px-3 border-top"
        style={{
          justifyContent: "space-around",
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            minWidth: "250px", minHeight: "60px"
          }}>
          <strong style={{ fontSize: "1.3rem" }}>ECRARM</strong>
          Element Classification Robot Arm
        </div>
        <div
          className="d-flex text-muted"
          style={{
            fontSize: "12px",
            justifyContent: "flex-start",
            justifyItems: "flex-start",
            alignItems: "center",
            alignContent: "center",
            minWidth: "250px",
            minHeight: "60px"

          }}
        >
          2022 Hanium ICT공모전 / 22hf_182 <br />
          © 김영희.박건하.이희원.차우석 all right reserved <br/>
          © Developed by GeonhaPark | seunmul
        </div>
      </footer>
    </>
  );
};

export default SignIn;
