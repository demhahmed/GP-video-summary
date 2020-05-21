import React, { Component } from "react";

import { Row, Col, Image } from "react-bootstrap";
import thumbnail from "../../assets/thumbnail.jpeg";
import { RiPlayCircleLine } from "react-icons/ri";
import "./SummaryCard.css";
import { Link } from "react-router-dom";

export default class SummaryCard extends Component {
  render() {
    return (
      <Link
        className="custom-link"
        to={`/summary_details/${this.props.summaryId}`}
      >
        <div
          className={`my-card ${this.props.small ? "small" : ""} ${
            this.props.verysmall ? "very-small" : ""
          }`}
        >
          <Image
            className="thumbnail-image"
            src={`/thumbnails/${this.props.thumbnail}`}
          />
          <RiPlayCircleLine
            className={`play-logo ${
              this.props.small || this.props.verysmall ? "small" : ""
            } `}
          />
          <div
            className={`my-card-scoreboard ${this.props.small ? "small" : ""} ${
              this.props.verysmall ? "very-small" : ""
            }`}
          >
            <Row>
              <Col xs={6}>
                <div className="team-image">
                  <Image
                    className={`homeTeam ${this.props.small ? "small" : ""} ${
                      this.props.verysmall ? "very-small" : ""
                    }`}
                    src={this.props.homeTeam}
                  />
                </div>
              </Col>
              <Col xs={6}>
                <div className="team-image">
                  <Image
                    className={`awayTeam ${this.props.small ? "small" : ""} ${
                      this.props.verysmall ? "very-small" : ""
                    }`}
                    src={this.props.awayTeam}
                  />
                </div>
              </Col>
            </Row>
          </div>
          <div
            className={`vs ${this.props.small ? "small" : ""} ${
              this.props.verysmall ? "very-small" : ""
            }`}
          >
            vs
          </div>
        </div>
      </Link>
    );
  }
}
