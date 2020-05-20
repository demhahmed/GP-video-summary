import React, { Component } from "react";
import { connect } from "react-redux";
import { Navbar, Nav, Image } from "react-bootstrap";
import SignInDropdown from "../Custom/SignInDropdown";
import { Link } from "react-router-dom";
import { FaCloud } from "react-icons/fa";
import logo from "../../assets/logo_2.svg";
import uploadLogo from "../../assets/upload.svg";

import "./Navigation.css";
class Navigation extends Component {
  render() {
    if (this.props.user) {
      console.log(this.props.user.image);
    }
    return (
      <Navbar className="col d-none d-sm-block dark-nav">
        <div className="container my-class">
          <Navbar.Brand>
            <Image height="40px" src={logo} />
          </Navbar.Brand>
          <Nav className="mr-sm-2">
            <Nav className=" mr-auto">
              <div className="upload-container">
                <div>
                  <Image className="uploadlogo" src={uploadLogo} /> <span>Upload</span>
                </div>
              </div>
            </Nav>
            <Nav className="mr-auto">
              <SignInDropdown />
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

export default connect(mapStateToProps, {})(Navigation);
