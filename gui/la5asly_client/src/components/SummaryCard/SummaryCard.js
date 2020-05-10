import React, { Component } from "react";

import { Card, Button, Row, Col, Image } from "react-bootstrap";
import moment from "moment";
import bundesliga from "../../images/b_l.png";
import ligue_1 from "../../images/l_1.png";
import premierleague from "../../images/p_l.png";
import la_liga from "../../images/la_liga.png";

export default class SummaryCard extends Component {
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
      <Card>
        <Image thumbnail variant="top" src={`http://localhost:3001/thumbnails/${this.props.thumbnail}`} />
        <Card.Body>
          <Row>
            <Col xs={3}>
              <Image
                width="50px"
                height="50px"
                roundedCircle
                src={this.props.user.image}
              />
            </Col>
            <Col xs={9}>
              <p>{this.props.title}</p>
            </Col>
          </Row>
          <Row>
            <Col xs={{ offset: 3 }}>
              <p>{this.props.username}</p>
            </Col>
          </Row>
          <Row>
            <Col xs={{ offset: 3 }}>
              <p>Uploaded at: {moment(new Date(this.props.createdAt), "YYYYMMDD").fromNow()}</p>
            </Col>
          </Row>
          <Row>
            <Col xs={{ offset: 3 }}>
              <p>
                League: <Image height="30px" width="30px" src={srcImg} /> {this.props.leagueType}
              </p>
            </Col>
          </Row>
        </Card.Body>
      </Card>
    );
  }
}
