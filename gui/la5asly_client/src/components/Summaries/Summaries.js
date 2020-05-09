import React, { Component } from "react";
import SummaryCard from "../SummaryCard";
import { Row, Col, Nav, Image, Button } from "react-bootstrap";
import { Link } from "react-router-dom";

import bundesliga from "../../images/b_l.png";
import ligue_1 from "../../images/l_1.png";
import premierleague from "../../images/p_l.png";
import la_liga from "../../images/la_liga.png";
import { AiOutlineFileAdd } from "react-icons/ai";
import "./Summaries.css";

export default class Summaries extends Component {
  render() {
    return (
      <div className="container">
        <div className="filter-tab"></div>
        <Nav fill variant="tabs">
          <Nav.Item>
            <Nav.Link eventKey="all" >All Leagues</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link eventKey="premierleague">
              <Image
                style={{ marginRight: "4px" }}
                width="32px"
                height="32px"
                src={premierleague}
              />
              Premier League
            </Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link eventKey="bundesliga">
              <Image
                style={{ marginRight: "4px" }}
                width="32px"
                height="32px"
                src={bundesliga}
              />
              Bundesliga
            </Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link eventKey="la_liga">
              <Image
                style={{ marginRight: "4px" }}
                width="32px"
                height="32px"
                src={la_liga}
              />
              La Liga
            </Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link eventKey="ligue_1">
              <Image
                style={{ marginTop: "-3px", marginRight: "4px" }}
                width="32px"
                height="40px"
                src={ligue_1}
              />
              Ligue 1
            </Nav.Link>
          </Nav.Item>
        </Nav>
        <Row style={{ marginTop: "20px" }}>
          <Col xs={{ offset: 10 }}>
            <Link className="custom-link" to="/uploadmatch">
              <Button variant="success" block>
                <AiOutlineFileAdd style={{ fontSize: "25px" }} /> Upload Match
              </Button>
            </Link>
          </Col>
        </Row>
        <Row>
          {[1, 2, 3, 4].map((element) => {
            return (
              <Col xs={4}>
                <div style={{ margin: "10px 0" }}>
                  <SummaryCard />
                </div>
              </Col>
            );
          })}
        </Row>
      </div>
    );
  }
}
