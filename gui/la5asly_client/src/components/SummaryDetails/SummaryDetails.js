import React, { Component } from "react";
import ReactPlayer from "react-player";
import { connect } from "react-redux";
import { Row, Col, Card, Image, ProgressBar } from "react-bootstrap";
import moment from "moment";
import { fetchSummaries, sendFeedback } from "../../actions";
import "react-input-range/lib/css/index.css";
import "./SummaryDetails.css";
import { Redirect } from "react-router-dom";
import homeImage from "../../assets/home.jpg";
import brokenHeart from "../../assets/broken heart.svg";
import love from "../../assets/love-and-romance.svg";
import InputRange from "react-input-range";
import { RiFeedbackLine } from "react-icons/ri";
class SummaryDetails extends Component {
  state = {
    value: 2,
  };

  async componentWillMount() {
    this.props.fetchSummaries();
  }

  calculateHappieness = (idx) => {
    const length = this.props.summaries[idx].versions[0].feedbacks.length;
    let value = 0;
    if (length === 0) return 0;
    this.props.summaries[idx].versions[0].feedbacks.forEach((feedback) => {
      value += feedback.feedback;
    });
    return (value / length / 5) * 100;
  };

  sendFeedback = (idx) => {
    this.props.sendFeedback(
      this.props.match.params.id,
      this.props.summaries[idx].versions[0]._id,
      this.props.user._id,
      this.state.value
    );
  };

  render() {
    const idx = this.props.summaries
      .map((summary) => summary._id)
      .indexOf(this.props.match.params.id);
    if (idx === -1) {
      return <Redirect to="/" />;
    }
    const value = this.calculateHappieness(idx);
    return (
      <div className="container">
        <Image className="bk-overlay" src={homeImage} />
        <div className="dark-overlay" />
        <div style={{ padding: "40px 0" }}>
          {idx !== -1 && (
            <Row>
              <Col xs={10}>
                <ReactPlayer
                  className="player"
                  url={`/summaries/${this.props.summaries[idx].summaryPath}`}
                  playing={false}
                  controls
                />
                <Row>
                  <Col style={{ marginTop: "12px" }} xs={6}>
                    <p>what users think about this summary</p>
                    <div className="progress-container">
                      <Image className="borken-heart" src={brokenHeart} />
                      <ProgressBar className="people-progress" now={value} />
                      <p
                        style={{
                          position: "absolute",
                          top: "-3px",
                          fontSize: "15px",
                          left: "172px",
                        }}
                      >
                        {value}%
                      </p>
                      <Image className="love" src={love} />
                    </div>
                  </Col>
                  {this.props.user.isLoggedIn &&
                    this.props.summaries[idx].versions[0].feedbacks.filter(
                      (feedback) => feedback.user._id === this.props.user._id
                    ).length === 0 && (
                      <Col style={{ marginTop: "12px" }} xs={6}>
                        <p>Send Feedback!</p>
                        <div className="progress-container">
                          <InputRange
                            maxValue={5}
                            minValue={0}
                            value={this.state.value}
                            onChange={(value) => this.setState({ value })}
                          />
                          <button
                            onClick={(e) => {
                              e.preventDefault();
                              this.sendFeedback(idx);
                            }}
                            className="my-btn feedback"
                          >
                            <RiFeedbackLine style={{ fontSize: "20px" }} /> Send
                          </button>
                        </div>
                      </Col>
                    )}
                </Row>
              </Col>
              <Col xs={2}>
                <Row>
                  <Col xs={6}>
                    <p style={{ fontSize: "22px" }} className="text-center">
                      Home
                    </p>
                  </Col>
                  <Col xs={6}>
                    <p style={{ fontSize: "22px" }} className="text-center">
                      Away
                    </p>
                  </Col>
                </Row>
                <Row>
                  <Col xs={6}>
                    <Image
                      className="details-logo"
                      src={this.props.summaries[idx].homeTeam.logo}
                    />
                  </Col>
                  <Col xs={6}>
                    <Image
                      className="details-logo"
                      src={this.props.summaries[idx].awayTeam.logo}
                    />
                  </Col>
                </Row>
                <div className="text-center details-section">
                  <p className="details-label">Goals</p>
                  <p className="details-result">
                    {this.props.summaries[idx].versions[0].goals}
                  </p>
                </div>
                <div className="text-center details-section">
                  <p className="details-label">Chances</p>
                  <p className="details-result">
                    {this.props.summaries[idx].versions[0].chances}
                  </p>
                </div>
                <div className="text-center details-section">
                  <p className="details-label">Length</p>
                  <p className="details-result">
                    {this.props.summaries[idx].versions[0].length} min
                  </p>
                </div>
              </Col>
            </Row>
          )}
        </div>
      </div>
    );
  }
}

const mapStateToProps = (store) => {
  return { summaries: store.summaries, user: store.user };
};

export default connect(mapStateToProps, { fetchSummaries, sendFeedback })(
  SummaryDetails
);
