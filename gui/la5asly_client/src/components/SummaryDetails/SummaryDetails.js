import React, { Component } from "react";
import ReactPlayer from "react-player";
import { connect } from "react-redux";
import { Row, Col, Card, Image } from "react-bootstrap";
import bundesliga from "../../images/b_l.png";
import ligue_1 from "../../images/l_1.png";
import premierleague from "../../images/p_l.png";
import la_liga from "../../images/la_liga.png";
import moment from "moment";

import "./SummaryDetails.css";

class SummaryDetails extends Component {
  render() {
    let srcImg;
    switch (this.props.leagueType) {
      case "La Liga":
        srcImg = la_liga;
        break;
      case "Premier League":
        srcImg = premierleague;
        break;
      case "Ligue 1":
        srcImg = ligue_1;
        break;
      case "BundesLiga":
        srcImg = bundesliga;
        break;
      default:
        break;
    }
    return (
      <div className="container">
        <Card style={{ marginTop: "20px" }}>
          <Card.Title>
            <h2 style={{ padding: "10px", fontWeight: "bold" }}>Match Info</h2>
          </Card.Title>
          <Row>
            <Col style={{ marginTop: "8px", marginBottom: "8px" }} xs={3}>
              <Image width="128px" src={srcImg} />
            </Col>
            <Col xs={9}>
              <Row>
                <Col xs={3}>
                  <h5 style={{ marginTop: "10px" }}>Uploader</h5>
                </Col>
                <Col xs={3}>
                  <h5 style={{ marginTop: "10px" }}>Uploaded At</h5>
                </Col>
                <Col xs={6}>
                  <h5 style={{ marginTop: "10px" }}>Title</h5>
                </Col>
              </Row>
              <Row>
                <Col xs={3}>
                  <Image
                    style={{ cursor: "pointer" }}
                    width="75px"
                    height="75px"
                    roundedCircle
                    src={srcImg}
                  />
                </Col>
                <Col xs={3}>
                  <p style={{ marginTop: "25px" }}>
                    {moment(this.props.createdAt, "YYYYMMDD").fromNow()}
                  </p>
                </Col>
                <Col xs={6}>
                  <p style={{ marginTop: "25px" }}>{this.props.title}</p>
                </Col>
              </Row>
            </Col>
          </Row>
        </Card>
        <Row style={{ marginTop: "20px" }}>
          <Col xs={6}>
            <div>
              <ReactPlayer
                url={`https://localhost:3001/summaries/${this.props.summaryPath}`}
                controls
              />
            </div>
          </Col>
          <Col xs={{ offset: 1 }}>
            <Card>
              <Card.Title>
                <h3 className="card-title-stat">Statistics</h3>
              </Card.Title>
              <Card.Body>
                <Card.Text>
                  <Row>
                    <Col xs={8}>
                      <h5>Goals</h5>
                    </Col>
                    <Col xs={4}>
                      <p>10</p>
                    </Col>
                  </Row>
                </Card.Text>
                <Card.Text>
                  <Row>
                    <Col xs={8}>
                      <h5>Dangerous Chances</h5>
                    </Col>
                    <Col xs={4}>
                      <p>10</p>
                    </Col>
                  </Row>
                </Card.Text>
                <Card.Text>
                  <Row>
                    <Col xs={8}>
                      <h5>Video Length</h5>
                    </Col>
                    <Col xs={4}>
                      <p>10 min</p>
                    </Col>
                  </Row>
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

const mapStateToProps = (store) => {
  return { user: store.user.user };
};

export default connect(mapStateToProps, {})(SummaryDetails);
