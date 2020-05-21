import React, { Component } from "react";

import "./Results.css";
import { connect } from "react-redux";
import { Row, Col, Pagination } from "react-bootstrap";
import SummaryCard from "../../SummaryCard";
import Loading from "../../Loading";

const getFilteredData = (store, ownProps) => {
  return store.summaries.filter((summary) => {
    let filter = true;
    if (ownProps.filters.search) {
      filter =
        filter &&
        (summary.homeTeam.name.toLowerCase().includes(ownProps.filters.search.toLowerCase()) ||
          summary.awayTeam.name.toLowerCase().includes(ownProps.filters.search.toLowerCase()) ||
          summary.leagueType.name.toLowerCase().includes(ownProps.filters.search.toLowerCase()));
    }
    if (ownProps.filters.date) {
      const date = new Date(summary.createdAt);
      const filterDate = new Date(ownProps.filters.date);
      filter =
        filter &&
        date.getDay() === filterDate.getDay() &&
        date.getMonth() === filterDate.getMonth() &&
        date.getFullYear() === filterDate.getFullYear();
    }
    if (ownProps.filters.league) {
      console.log(summary.leagueType._id === ownProps.filters.league)
      filter = filter && summary.leagueType._id === ownProps.filters.league;
    }
    return filter;
  });
};

class Results extends Component {
  state = {
    page: 1,
    wait: false,
  };
  renderPages = () => {
    if (!this.props.summaries) return [];
    let items = [];
    for (
      let number = 1;
      number <= Math.ceil(this.props.summaries.length / 12);
      number++
    ) {
      items.push(
        <Pagination.Item
          onClick={() => {
            this.setState({ wait: true }, () => {
              setTimeout(() => {
                this.setState({ page: number, wait: false });
              }, 2000);
            });
          }}
          key={number}
          active={number === this.state.page}
        >
          {number}
        </Pagination.Item>
      );
    }
    if (items.length === 1) return [];
    return items;
  };

  render() {
    return (
      <div>
        <div className="home-header">
          <span>Results</span>
        </div>
        {this.state.wait && <Loading />}
        {!this.state.wait && (
          <Row>
            {this.props.summaries
              .slice(
                (this.state.page - 1) * 12,
                (this.state.page - 1) * 12 + 12
              )
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
        )}
        <Pagination>{this.renderPages()}</Pagination>
      </div>
    );
  }
}

const mapStateToProps = (store, ownProps) => {
  return {
    summaries: getFilteredData(store, ownProps),
  };
};

export default connect(mapStateToProps, {})(Results);
