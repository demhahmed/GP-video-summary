import React, { Component } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { Image, Row, Col, Button } from "react-bootstrap";
import { showNotification, hideNotification } from "../../actions";

import homeImage from "../../assets/home.jpg";

import "./Home.css";
import { FaFire, FaVideo, FaCalendarDay } from "react-icons/fa";
import SummaryCard from "../SummaryCard";
import HomeFilterForm from "./HomeFilterForm";
import Results from "./Results/Results";

class Home extends Component {
  state = {
    filter: true,
  };
  render() {
    return (
      <div className="container">
        <Image className="bk-overlay" src={homeImage} />
        <div className="dark-overlay" />
        <section>
          <HomeFilterForm />
        </section>
        {this.state.filter ? (
          <Results />
        ) : (
          <div>
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
              {this.props.teams && (
                <button
                  style={{ display: "block", margin: "70px auto 0px" }}
                  className="my-btn"
                >
                  View More
                </button>
              )}
            </section>
            <section className="my-section">
              <div className="home-header">
                <span>Popular</span>
              </div>
              {this.props.teams && (
                <Row>
                  {this.props.teams
                    .slice(8, Math.min(20, this.props.teams.length))
                    .map((team) => (
                      <Col xs={3}>
                        <SummaryCard
                          verysmall={true}
                          homeTeam={team.logo}
                          awayTeam={team.logo}
                        />
                      </Col>
                    ))}
                </Row>
              )}
              {this.props.teams && (
                <button
                  style={{ display: "block", margin: "20px auto" }}
                  className="my-btn"
                >
                  View More
                </button>
              )}
            </section>
          </div>
        )}
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
