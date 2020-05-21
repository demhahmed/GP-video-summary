import React, { Component } from "react";
import { Image } from "react-bootstrap";
import aboutImage from "../../assets/about.jpg";
export default class About extends Component {
  render() {
    return (
      <div className="container">
        <Image className="bk-overlay" src={aboutImage} />
        <div className="dark-overlay" />
        <div className="home-header">
          <span>About</span>
        </div>
        <p
          style={{ fontSize: "22px" }}
          className="lead"
        >
          LAخSLY is an automatic soccer video summarization system that uses a
          variety of techniques in the fields of image processing and machine
          learning to produce high quality summaries of soccer matches in
          different lengths to save the user's time and enrich the viewing
          experience.
        </p>
      </div>
    );
  }
}
