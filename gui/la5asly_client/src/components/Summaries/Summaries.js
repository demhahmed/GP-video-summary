import React, { Component } from "react";
import SummaryCard from "../SummaryCard";
import { Row, Col, Nav, Image, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import { connect } from "react-redux";

import { fetchSummaries } from "../../actions";

import bundesliga from "../../images/b_l.png";
import ligue_1 from "../../images/l_1.png";
import premierleague from "../../images/p_l.png";
import la_liga from "../../images/la_liga.png";
import { AiOutlineFileAdd } from "react-icons/ai";
import "./Summaries.css";

class Summaries extends Component {

  state = {
    filter: null
  }

  componentDidMount() {
    this.props.fetchSummaries({})
  }

  handleFilter = (type) => {
    if (type == "all") {
      this.setState({ filter: null })
    } else {
      this.setState({ filter: type })

    }
  }

  render() {
    return (
      <div className="container">
        <div className="filter-tab"></div>
        <Nav fill variant="tabs">
          <Nav.Item>
            <Nav.Link onClick={() => this.handleFilter("all")} eventKey="all">All Leagues</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link onClick={() => this.handleFilter("Premier League")} eventKey="premierleague">
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
            <Nav.Link onClick={() => this.handleFilter("BundesLiga")} eventKey="bundesliga">
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
            <Nav.Link onClick={() => this.handleFilter("La Liga")} eventKey="la_liga">
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
            <Nav.Link onClick={() => this.handleFilter("Ligue 1")} eventKey="ligue_1">
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
        {this.props.user && (
          <Row style={{ marginTop: "20px" }}>
            <Col xs={{ offset: 10 }}>
              <Link className="custom-link" to="/uploadmatch">
                <Button variant="success" block>
                  <AiOutlineFileAdd style={{ fontSize: "25px" }} /> Upload Match
                </Button>
              </Link>
            </Col>
          </Row>
        )}
        <Row>
          {this.props.summaries.filter(element => {
            if (this.state.filter) {
              return element.leagueType === this.state.filter;
            } else {
              return true;
            }
          }).map((element) => {
            return (
              <Col xs={4}>
                <div style={{ margin: "10px 0" }}>
                  <Link
                    style={{ textDecoration: "none" }}
                    to={`/summary_details/${element._id}`}
                  >
                    <SummaryCard {...element} />
                  </Link>
                </div>
              </Col>
            );
          })}
        </Row>
      </div>
    );
  }
}

const mapStateToProps = (store) => {
  return { user: store.user.user, summaries: store.summaries.summaries };
};

export default connect(mapStateToProps, { fetchSummaries })(Summaries);
