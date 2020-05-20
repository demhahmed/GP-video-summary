import React, { Component } from "react";
import { Form, FormControl, Button, Row, Col } from "react-bootstrap";

import "./HomeFilterForm.css";
import { FaSearch } from "react-icons/fa";
import LeagueDropdown from "../Custom/LeagueDropdown/LeagueDropdown";
import { connect } from "react-redux";
class HomeFilterForm extends Component {
  render() {
    return (
      <div>
        <Form>
          <div className="search-bar-container">
            <div className="search-placeholder">Search</div>
            <FormControl
              type="text"
              className="my-search"
              placeholder="Enter text to search for"
            />
            <FaSearch className="search-icon" />
          </div>
          <div className="filters">
            <Row>
              <Col xs={6}>
                <LeagueDropdown leagues />
              </Col>
            </Row>
          </div>
        </Form>
      </div>
    );
  }
}

export default HomeFilterForm;
