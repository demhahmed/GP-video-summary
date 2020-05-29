import React, { Component } from "react";

import { Row, Col, Image, ProgressBar } from "react-bootstrap";
import thumbnail from "../../assets/thumbnail.jpeg";
import { RiPlayCircleLine } from "react-icons/ri";
import "./SummaryCard.css";
import { Link, withRouter } from "react-router-dom";

class SummaryCard extends Component {
  onSummaryCardClick = (e) => {
    e.preventDefault();
    if (this.props.complete) {
      this.props.history.push(`/summary_details/${this.props.summaryId}`);
    }
  };
  render() {
    return (
      <div>
        <Link
          className={`custom-link`}
          onClick={this.onSummaryCardClick}
          to={`/summary_details/${this.props.summaryId}`}
        >
          <div
            className={`my-card ${this.props.small ? "small" : ""} ${
              this.props.verysmall ? "very-small" : ""
            }`}
          >
            <Image
              className="thumbnail-image"
              src={`/thumbnails/${this.props.thumbnail}?t=${new Date().getTime()}`}
            />

            {!this.props.complete && <div className="dark-overlay-card" />}
            {!this.props.complete && (
              <div className="progress-card">
                <ProgressBar now={this.props.progress} />
                <p className="progress-card-label">{this.props.progress}%</p>
              </div>
            )}
            {this.props.complete && (
              <RiPlayCircleLine
                className={`play-logo ${
                  this.props.small || this.props.verysmall ? "small" : ""
                } `}
              />
            )}

            <div
              className={`${this.props.complete ? "" : "not-complete"} `}
            ></div>
            <div
              className={`my-card-scoreboard ${
                this.props.small ? "small" : ""
              } ${this.props.verysmall ? "very-small" : ""}`}
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
      </div>
    );
  }
}
export default withRouter(SummaryCard);
