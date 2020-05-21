import React, { Component } from "react";

import "./Results.css";
import { connect } from "react-redux";
import { Row, Col, Pagination } from "react-bootstrap";
import SummaryCard from "../../SummaryCard";
import Loading from "../../Loading";

class Results extends Component {
  state = {
    page: 1,
    wait: false,
  };
  renderPages = () => {
    if (!this.props.teams) return [];
    let items = [];
    for (
      let number = 1;
      number <= Math.ceil(this.props.teams.length / 12);
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
            {this.props.teams &&
              this.props.teams
                .slice(
                  (this.state.page - 1) * 12,
                  (this.state.page - 1) * 12 + 12
                )
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
        <Pagination>{this.renderPages()}</Pagination>
      </div>
    );
  }
}

const mapStateToProps = (store) => {
  return {
    teams: store.teams.teams,
  };
};

export default connect(mapStateToProps, {})(Results);
