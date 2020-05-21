import React, { Component } from "react";
import "./Footer.css";
import { Row, Col } from "react-bootstrap";
import { FaFacebook, FaInstagram, FaLinkedin, FaTwitter } from "react-icons/fa";
export default class Footer extends Component {
  render() {
    return (
      <div className="footer">
        <div className="container">
          <Row>
            <Col xs={3}>
              <h2>Pages</h2>
              <ul>
                <li>Home</li>
                <li>About Us</li>
              </ul>
            </Col>
            <Col xs={3}>
              <h2>Contact Us</h2>
              <ul>
                <li>asivo.ahmed@gmail.com</li>
                <li>demha.ahmed@yahoo.com</li>
                <li>MoamenAttia@outlook.com</li>
                <li>mohamedtalaat0111790@gmail.com</li>
              </ul>
            </Col>
            <Col xs={3}>
              <h2>Information</h2>
              <ul>
                <li>Work With Us</li>
                <li>Privacy Policy</li>
                <li>Terms &amp; Conditions</li>
              </ul>
            </Col>
            <Col xs={3}>
              <h2>Follow Us</h2>
              <ul className="social-media">
                <li>
                  <a
                    target="_blank"
                    href="https://www.facebook.com/marshal.moamen"
                  >
                    <FaFacebook className="text-primary" />
                  </a>
                </li>
                <li>
                  <a
                    target="_blank"
                    href="https://www.instagram.com/marshal_moamen/"
                  >
                    <FaInstagram className="text-danger" />
                  </a>
                </li>
                <li>
                  <a
                    target="_blank"
                    href="https://www.linkedin.com/in/moamen-attia/"
                  >
                    <FaLinkedin className="text-linkedin" />
                  </a>
                </li>
                <li>
                  <a target="_blank" href="https://twitter.com/MarshalMoamen">
                    <FaTwitter className="text-info" />
                  </a>
                </li>
              </ul>
            </Col>
          </Row>
        </div>
        <p className="footer-copyright lead text-center"><span>La5asly</span>, &copy; {new Date().getFullYear()} Copyright</p>
      </div>
    );
  }
}
