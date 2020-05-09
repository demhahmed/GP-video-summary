import React, { Component } from "react";
import { Navbar, Form, FormControl, Button, Nav, Image } from "react-bootstrap";
import { Link } from "react-router-dom";
import "./Navigation.css";
import { IoIosFootball, IoLogoGoogle } from "react-icons/io";
import GoogleLogin from "react-google-login";
class Navigation extends Component {
  responseSuccessGoogle = (response) => console.log(response);
  responseFailGoogle = (response) => console.log(response);

  render() {
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
            <GoogleLogin
              clientId="1024627819936-egebh5n0541fciddrtkrdnc8q3ju1snk.apps.googleusercontent.com"
              buttonText="Login"
              render={(renderProps) => (
                <Button {...renderProps} block type="submit" variant="danger">
                  <IoLogoGoogle className="custom-google-icon" /> Login with Google
                </Button>
              )}
              onSuccess={this.responseSuccessGoogle}
              onFailure={this.responseFailGoogle}
              isSignedIn={true}
            />
          </Nav>
        </div>
      </Navbar>
    );
  }
}

export default Navigation;
