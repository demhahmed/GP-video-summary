import React, { Component } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { Image, Row, Col, Button } from "react-bootstrap";
import { showNotification, hideNotification } from "../../actions";

import homeImage from "../../assets/home.jpg";

import "./Home.css";
import SummaryCard from "../SummaryCard";
import HomeFilterForm from "./HomeFilterForm";
import Results from "./Results/Results";
import { FaBackspace } from "react-icons/fa";

class Home extends Component {
  state = {
    filter: false,
    filters: {},
  };
  onSearchClick = () => {
    const { date, search, league } = this.props.filterForm.values;
    this.setState({ filter: true, filters: { date, search, league } });
  };

  onClearFiltersClick = () => {
    this.setState({ filter: false });
  };
  render() {
    const todaySummaries = this.props.summaries.filter((summary) => {
      const date = new Date(summary.createdAt);
      const today = new Date();
      return (
        date.getDay() === today.getDay() &&
        date.getMonth() === today.getMonth() &&
        date.getFullYear() === today.getFullYear()
      );
    });
    const notTodaySummaries = this.props.summaries.filter((summary) => {
      const date = new Date(summary.createdAt);
      const today = new Date();
      return !(
        date.getDay() === today.getDay() &&
        date.getMonth() === today.getMonth() &&
        date.getFullYear() === today.getFullYear()
      );
    });
    return (
      <div className="container">
        <Image className="bk-overlay" src={homeImage} />
        <div className="dark-overlay" />
        <section>
          <HomeFilterForm
            onSearchClick={this.onSearchClick}
            onClearFiltersClick={this.onClearFiltersClick}
            filter={this.state.filter}
          />
        </section>
        {this.state.filter ? (
          <Results filter={this.state.filter} filters={this.state.filters} />
        ) : (
          <div>
            {todaySummaries.length > 0 && (
              <div style={{ paddingBottom: "40px" }}>
                <section>
                  <div className="home-header">
                    <span>Today</span>
                  </div>
                  <Row>
                    <Col xs={6}>
                      <SummaryCard
                        homeTeam={todaySummaries[0].homeTeam.logo}
                        awayTeam={todaySummaries[0].awayTeam.logo}
                        thumbnail={todaySummaries[0].thumbnail}
                        summaryId={todaySummaries[0]._id}
                      />
                    </Col>
                    <Col xs={6}>
                      <Row>
                        {todaySummaries
                          .slice(1, Math.min(todaySummaries.length, 5))
                          .map((summary) => (
                            <Col xs={6}>
                              <SummaryCard
                                small={true}
                                homeTeam={summary.homeTeam.logo}
                                awayTeam={summary.awayTeam.logo}
                                thumbnail={summary.thumbnail}
                                summaryId={summary._id}
                              />
                            </Col>
                          ))}
                      </Row>
                    </Col>
                  </Row>
                  {todaySummaries.length > 5 && (
                    <button
                      onClick={(e) => {
                        e.preventDefault();
                        this.setState({
                          filters: { date: new Date() },
                          filter: true,
                        });
                      }}
                      style={{ display: "block", margin: "70px auto 20px" }}
                      className="my-btn"
                    >
                      View More
                    </button>
                  )}
                </section>
              </div>
            )}
            {notTodaySummaries.length > 0 && (
              <section className="my-section">
                <div className="home-header">
                  <span>Popular</span>
                </div>
                <Row>
                  {notTodaySummaries
                    .slice(0, Math.min(12, notTodaySummaries.length))
                    .map((summary) => (
                      <Col xs={3}>
                        <SummaryCard
                          verysmall={true}
                          homeTeam={summary.homeTeam.logo}
                          awayTeam={summary.awayTeam.logo}
                          thumbnail={summary.thumbnail}
                          summaryId={summary._id}
                        />
                      </Col>
                    ))}
                </Row>
                {notTodaySummaries.length > 12 && (
                  <button
                    onClick={() => this.setState({ filter: true })}
                    style={{ display: "block", margin: "20px auto" }}
                    className="my-btn"
                  >
                    View More
                  </button>
                )}
              </section>
            )}
            {todaySummaries.length === 0 && notTodaySummaries.length === 0 && (
              <div>
                <p style={{ marginTop: "47px" }} className="lead text-center">
                  No Summaries found
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    );
  }
}

const mapStateToProps = (store) => {
  return {
    user: store.user,
    teams: store.teams.teams,
    summaries: store.summaries,
    filterForm: store.form.FilterForm,
  };
};

export default connect(mapStateToProps, { showNotification, hideNotification })(
  Home
);
