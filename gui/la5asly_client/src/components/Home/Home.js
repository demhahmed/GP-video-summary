import React, { Component } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { Image, Row, Col } from "react-bootstrap";
import { showNotification, hideNotification } from "../../actions";

import homeImage from "../../assets/home.jpg";
import Summaries from "../Summaries";

import "./Home.css";
import { FaFire, FaVideo, FaCalendarDay } from "react-icons/fa";
import SummaryCard from "../SummaryCard";
import HomeFilterForm from "../HomeFilterForm";

class Home extends Component {
  render() {
    return (
      <div className="container">
        <Image className="bk-overlay" src={homeImage} />
        <div className="dark-overlay" />
        <section>
          <HomeFilterForm />
        </section>
        <section>
          <div className="home-header">
            <span>Today</span>
          </div>

          {this.props.teams && this.props.teams.length && (
            <Row>
              <Col xs={6}>
                <SummaryCard
                  homeTeam={this.props.teams[0].logo}
                  awayTeam={this.props.teams[0].logo}
                />
              </Col>
              <Col xs={6}>
                <Row>
                  {this.props.teams
                    .slice(8, Math.min(12, this.props.teams.length))
                    .map((team) => (
                      <Col xs={6}>
                        <SummaryCard
                          small={true}
                          homeTeam={team.logo}
                          awayTeam={team.logo}
                        />
                      </Col>
                    ))}
                </Row>
              </Col>
            </Row>
          )}
        </section>
        <div className="home-header">
          <FaFire className="home-header-icon" />
          <span>Popular</span>
        </div>
      </div>
    );
  }
}

const mapStateToProps = (store) => {
  return { user: store.user, teams: store.teams.teams };
};

export default connect(mapStateToProps, { showNotification, hideNotification })(
  Home
);
