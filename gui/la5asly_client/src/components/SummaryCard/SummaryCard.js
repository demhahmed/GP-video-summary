import React, { Component } from "react";

import { Card, Button, Row, Col, Image } from "react-bootstrap";
import moment from "moment";
import bundesliga from "../../images/b_l.png";
import ligue_1 from "../../images/l_1.png";
import premierleague from "../../images/p_l.png";
import la_liga from "../../images/la_liga.png";

export default class SummaryCard extends Component {
  render() {
    return (
      <Card>
        <Image thumbnail variant="top" src="http://localhost:3001/thumbnails/1.jpg" />
        <Card.Body>
          <Row>
            <Col xs={3}>
              <Image
                width="50px"
                height="50px"
                roundedCircle
                src={this.props.userImage}
              />
            </Col>
            <Col xs={9}>
              <p>شاهد ملخص مباراه العمر بين فيكر ومؤمن</p>
            </Col>
          </Row>
          <Row>
            <Col xs={{ offset: 3 }}>
              <p>{this.props.username}</p>
            </Col>
          </Row>
          <Row>
            <Col xs={{ offset: 3 }}>
              <p>Uploaded at: {moment("20200509", "YYYYMMDD").fromNow()}</p>
            </Col>
          </Row>
          <Row>
            <Col xs={{ offset: 3 }}>
              <p>
                League: <Image height="30px" width="30px" src={premierleague} /> Premier League
              </p>
            </Col>
          </Row>
        </Card.Body>
      </Card>
    );
  }
}
