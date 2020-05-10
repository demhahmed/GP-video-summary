import React, { Component } from "react";
import { connect } from "react-redux";
import { Navbar, Form, FormControl, Button, Nav, Image } from "react-bootstrap";
import { Link } from "react-router-dom";
import "./Navigation.css";
import { IoIosFootball, IoLogoGoogle } from "react-icons/io";
import { signIn, signOut } from "../../actions";

class Navigation extends Component {
  componentWillMount() {
    window.gapi.load("client:auth2", () => {
      window.gapi.client
        .init({
          clientId:
            "1024627819936-egebh5n0541fciddrtkrdnc8q3ju1snk.apps.googleusercontent.com",
          scope: 'email',
        })
        .then(() => {
          this.auth = window.gapi.auth2.getAuthInstance();
          this.onAuthChange(this.auth.isSignedIn.get());
          this.auth.isSignedIn.listen(this.onAuthChange);
        });
    });
  }

  onAuthChange = (isSignedIn) => {
    if (isSignedIn) {
      const username = this.auth.currentUser.get().getBasicProfile().getName();
      const userId = this.auth.currentUser.get().getBasicProfile().getId();
      const image = this.auth.currentUser.get().getBasicProfile().getImageUrl();
      this.props.signIn(userId, username, image);
    } else {
      this.props.signOut();
    }
  };

  onSignInClick = () => {
    this.auth.signIn();
  };

  onSignOutClick = () => {
    this.auth.signOut();
  };

  renderAuthButton() {
    if (this.props.isSignedIn === null) {
      return null;
    }
    if (this.props.user) {
      return (
        <button onClick={this.onSignOutClick} className="ui red google button">
          <i className="google icon" />
          Sign out
        </button>
      );
    } else {
      return (
        <button onClick={this.onSignInClick} className="ui red google button">
          <i className="google icon" />
          Sign In with Google
        </button>
      );
    }
  }


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
            {this.props.user && (
              <Nav className="mr-auto">
                <Link
                  className="custom-link accent-hover-class"
                  to="/my_uploads"
                >
                  <div className="link" style={{ marginRight: "20px" }}>
                    My Uploads
                  </div>
                </Link>
              </Nav>
            )}
            {this.props.user && (
              <Nav className="mr-auto">
                <Link
                  onClick={this.onSignOutClick}
                  className="custom-link accent-hover-class"
                  to="/my_uploads"
                >
                  <div className="link" style={{ marginRight: "20px" }}>
                    Log out
                  </div>
                </Link>
              </Nav>
            )}
            {this.props.user && (
              <Nav className="mr-auto">
                <Image
                  width="40px"
                  height="40px"
                  roundedCircle
                  src={this.props.user.image}
                />
              </Nav>
            )}
            {this.props.isSignedIn !== null && !this.props.user && (
              <Nav className="mr-auto">
                <Button onClick={this.onSignInClick} block type="submit" variant="danger">
                  <IoLogoGoogle className="custom-google-icon" /> Login with
                  Google
                </Button>
              </Nav>
            )}
          </Nav>
        </div>
      </Navbar>
    );
  }
}

const mapStateToProps = (store) => {
  return { user: store.user.user };
};

export default connect(mapStateToProps, { signIn, signOut })(Navigation);
