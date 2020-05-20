import React, { Component } from "react";

import { Row, Col, Image } from "react-bootstrap";
import thumbnail from '../../assets/thumbnail.jpeg'
import "./SummaryCard.css";

export default class SummaryCard extends Component {
  render() {
    return (
      <div className={`my-card ${this.props.small ? "small" : ""}`}>
        <Image
          className="thumbnail-image"
          src={thumbnail}
        />
        <div
          className={`my-card-scoreboard ${this.props.small ? "small" : ""}`}
        >
          <Row>
            <Col xs={6}>
              <div className="team-image">
                <Image
                  className={`homeTeam ${this.props.small ? "small" : ""}`}
                  src={this.props.homeTeam}
                />
              </div>
            </Col>
            <Col xs={6}>
              <div className="team-image">
                <Image
                  className={`awayTeam ${this.props.small ? "small" : ""}`}
                  src={this.props.awayTeam}
                />
              </div>
            </Col>
          </Row>
        </div>
        <div className={`vs ${this.props.small ? "small" : ""}`}>vs</div>
      </div>
    );
  }
}
