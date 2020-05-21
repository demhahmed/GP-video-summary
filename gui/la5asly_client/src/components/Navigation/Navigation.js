import React, { Component } from "react";
import { connect } from "react-redux";
import { Navbar, Nav, Image } from "react-bootstrap";
import SignInDropdown from "../Custom/SignInDropdown";
import { Link } from "react-router-dom";
import { FaCloud } from "react-icons/fa";
import logo from "../../assets/logo_2.svg";
import uploadLogo from "../../assets/upload.svg";
import avatar from "../../assets/avatar.png";

import { logOut } from "../../actions";

import "./Navigation.css";
class Navigation extends Component {
  state = {
    didLoad: false,
  };
  handleLogOut = () => {
    this.props.logOut();
  };

  render() {
    const style = this.state.didLoad ? {} : { visibility: "hidden" };

    return (
      <Navbar className="col d-none d-sm-block dark-nav">
        <div className="container my-class">
          <Link to="/" className="custom-link">
            <Navbar.Brand>
              <Image height="40px" src={logo} />
            </Navbar.Brand>
          </Link>
          <Nav className="mr-sm-2">
            <Nav className=" mr-auto">
              <Link className="custom-link" to="/about">
                <div className="upload-container">
                  <div>
                    <p style={{ marginTop: "8px" }}>About</p>
                  </div>
                </div>
              </Link>
            </Nav>
            {this.props.user.type === "admin" && (
              <Nav className=" mr-auto">
                <Link className="custom-link" to="/uploadmatch">
                  <div className="upload-container">
                    <div>
                      <Image className="uploadlogo" src={uploadLogo} />{" "}
                      <span>Upload</span>
                    </div>
                  </div>
                </Link>
              </Nav>
            )}
            <Nav className="mr-auto">
              {this.props.user.isLoggedIn && (
                <div className="upload-container">
                  <div onClick={this.handleLogOut}>
                    <p style={{ marginTop: "8px" }}>Log out</p>
                  </div>
                </div>
              )}
            </Nav>
            <Nav className="mr-auto">
              {!this.props.user.isLoggedIn && <SignInDropdown />}
              {this.props.user.isLoggedIn && (
                <Image roundedCircle className="avatar" src="/api/me/avatar" />
              )}
            </Nav>
          </Nav>
        </div>
      </Navbar>
    );
  }
}

const mapStateToProps = (store) => {
  return { user: store.user };
};

export default connect(mapStateToProps, { logOut })(Navigation);
