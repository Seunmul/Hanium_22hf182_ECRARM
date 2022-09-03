import React from "react";

const Login = () => {
  return (
    <div className="bg-default">
      <div className="main-content">
        {/* <!-- navigation --> */}
        <nav
          id="navbar-main"
          className="navbar navbar-horizontal navbar-transparent navbar-main navbar-expand-lg navbar-light"
        >
          <div className="container">
            <a className="navbar-brand" href="#">
              <img
                src="../static/legacy/assets/img/brand/white.png"
                alt="Argon Design - Template Starter Logo."
              />
            </a>
            <button
              className="navbar-toggler"
              type="button"
              data-toggle="collapse"
              data-target="#navbar-collapse"
              aria-controls="navbar-collapse"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div
              className="navbar-collapse navbar-custom-collapse collapse"
              id="navbar-collapse"
            >
              <div className="navbar-collapse-header">
                <div className="row">
                  <div className="col-6 collapse-brand">
                    <a href="/">
                      <img src="../static/legacy/assets/img/brand/blue.png" />
                    </a>
                  </div>
                  <div className="col-6 collapse-close">
                    <button
                      type="button"
                      className="navbar-toggler"
                      data-toggle="collapse"
                      data-target="#navbar-collapse"
                      aria-controls="navbar-collapse"
                      aria-expanded="false"
                      aria-label="Toggle navigation"
                    ></button>
                  </div>
                </div>
              </div>
              <ul className="navbar-nav mr-auto">
                <li className="nav-item">
                  <a className="nav-link">
                    <span className="nav-link-inner--text">Login</span>
                  </a>
                </li>
                <li className="nav-item">
                  <a className="nav-link">
                    <span className="nav-link-inner--text">Register</span>
                  </a>
                </li>
              </ul>
              <hr className="d-lg-none" />
              <ul className="navbar-nav align-items-lg-center ml-lg-auto">
                <li className="nav-item">
                  <a
                    className="nav-link nav-link-icon"
                    href="#"
                    target="_blank"
                    data-toggle="tooltip"
                    data-original-title="Like us on Facebook"
                  >
                    <i className="fab fa-facebook-square"></i>
                    <span className="nav-link-inner--text d-lg-none">
                      Facebook
                    </span>
                  </a>
                </li>
                <li className="nav-item">
                  <a
                    className="nav-link nav-link-icon"
                    href="#"
                    target="_blank"
                    data-toggle="tooltip"
                    data-original-title="Follow us on Twitter"
                  >
                    <i className="fab fa-twitter-square"></i>
                    <span className="nav-link-inner--text d-lg-none">
                      Twitter
                    </span>
                  </a>
                </li>
                <li className="nav-item d-none d-lg-block ml-lg-4">
                  <a
                    href="/react"
                    target="_blank"
                    className="btn btn-neutral btn-icon"
                  >
                    <span className="btn-inner--icon">
                      <i className="fas fa-rocket mr-2"></i>
                    </span>
                    <span className="nav-link-inner--text">Contact us</span>
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        {/* <!-- Header --> */}
        <div className="header bg-gradient-primary py-7 py-lg-8">
          <div className="container">
            <div className="header-body text-center mb-3">
              <div className="row justify-content-center">
                <div className="col-lg-5 col-md-6">
                  <p className="text-left text-bold text-white">
                    [2022 한이음 ICT 공모전]
                  </p>
                  <h1 className="text-white text-large">
                    <a target="" className="text-white" href="#">
                      ECRARM WEB DASHBOARD
                    </a>
                  </h1>
                </div>
              </div>
            </div>
          </div>
          <div className="separator separator-bottom separator-skew zindex-100">
            <svg
              x="0"
              y="0"
              viewBox="0 0 2560 100"
              preserveAspectRatio="none"
              version="1.1"
              xmlns="http://www.w3.org/2000/svg"
            >
              <polygon
                className="fill-default"
                points="2560 0 2560 100 0 100"
              ></polygon>
            </svg>
          </div>
        </div>

        {/* <!-- Page content --> */}
        <div className="container mt--8 pb-5">
          <div className="row justify-content-center">
            <div className="col-lg-5 col-md-7">
              <div className="card bg-secondary shadow border-0">
                <div className="card-header bg-transparent pb-3">
                  <h2 className="text-center mt-2 mb-2">LOGIN</h2>
                  <div className="text-center text-muted">
                    Add your credentials
                  </div>
                </div>
                <div className="card-body px-lg-5 py-lg-5">
                  <div>
                    <div className="form-group mb-3">
                      <div className="input-group input-group-alternative">
                        <div className="input-group-prepend">
                          <span className="input-group-text">
                            <i className="ni ni-single-02"></i>
                          </span>
                        </div>
                        <input
                          type="text"
                          placeholder="Username"
                          className="form-control"
                        />
                      </div>
                    </div>
                    <div className="form-group">
                      <div className="input-group input-group-alternative">
                        <div className="input-group-prepend">
                          <span className="input-group-text">
                            <i className="ni ni-lock-circle-open"></i>
                          </span>
                        </div>
                        <input
                          type="password"
                          placeholder="UserPassWord"
                          className="form-control"
                        />
                      </div>
                    </div>

                    <div className="text-center">
                      <a href="/home">
                        <button
                          type="submit"
                          name="login"
                          className="btn btn-primary my-4"
                        >
                          Sign in
                        </button>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
              <div className="row mt-3 text-center">
                <div className="col-12">
                  <a className="text-light">
                    <small>Create new account</small>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* <!-- footer --> */}

        <footer className="py-5">
          <div className="container">
            <div className="row align-items-center justify-content-xl-between">
              <div className="col-xl-6">
                <div className="copyright text-center text-xl-left text-muted">
                  <span href="#" className="font-weight-bold" target="_blank">
                    Contributor
                  </span>
                  <p className="text-lead text-bold text-white">
                    22_HF182 : 딥러닝 기반 객체인식 소자분류로봇
                    <br />- 김영희, 박건하, 이희원, 차우석 -
                  </p>
                </div>
              </div>
              <div className="col-xl-6">
                <div className="text-center text-xl-right text-muted">
                  &copy;
                  <a target="_blank" href="#">
                    Creative-Tim
                  </a>
                  - coded by
                  <a target="_blank" href="">
                    AppSeed
                  </a>
                </div>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default Login;
