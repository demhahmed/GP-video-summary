import React, { Component } from "react";
import { connect } from "react-redux";
import { Navbar, Form, FormControl, Button, Nav, Image } from "react-bootstrap";
import { Link } from "react-router-dom";
import "./Navigation.css";
import { IoIosFootball, IoLogoGoogle } from "react-icons/io";

class Navigation extends Component {
  render() {
    if (this.props.user) {
      console.log(this.props.user.image);
    }
    return (
      <Navbar bg="light" variant="light">
        <div className="container my-class">
          <Navbar.Brand style={{ color: "#C55A11" }}>
            <IoIosFootball style={{ fontSize: "42px" }} />
            La5asly
          </Navbar.Brand>
          <Nav className="mr-auto">
            <Link className="custom-link accent-hover-class" to="/">
              <div className="link">Home</div>
            </Link>
          </Nav>
          <Nav className="mr-sm-2">
            {!this.props.user.isLoggedIn && (
              <Nav className="mr-auto">
                <li>
                  <a href="/auth/google">Login With Google</a>
                </li>
              </Nav>
            )}
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
