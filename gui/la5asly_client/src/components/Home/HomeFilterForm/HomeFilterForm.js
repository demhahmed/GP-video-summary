import React, { Component } from "react";
import { Form, FormControl, Button, Row, Col } from "react-bootstrap";

import { FaSearch, FaBackspace } from "react-icons/fa";
import LeagueDropdown from "../../Custom/LeagueDropdown/LeagueDropdown";
import { DateTimePicker } from "react-widgets";
import momentLocaliser from "react-widgets-moment";

import moment from "moment";
import { connect } from "react-redux";
import { Field, reduxForm } from "redux-form";
import "react-widgets/dist/css/react-widgets.css";
import "./HomeFilterForm.css";

momentLocaliser(moment);

const renderSearch = ({
  input,
  label,
  placeholder,
  type,
  meta: { touched, error },
}) => {
  return (
    <div>
      <FormControl
        type="text"
        {...input}
        autoComplete="off"
        className="my-search"
        placeholder="Enter text to search for"
      />
      <FaSearch className="search-icon" />
    </div>
  );
};

const renderDropdown = ({ input: { onChange, value } }) => {
  return <LeagueDropdown onChange={onChange} />;
};

const renderDateTimePicker = ({
  input: { onChange, value },
  meta: { touched, error },
  showTime,
}) => {
  return (
    <div>
      <DateTimePicker
        onChange={onChange}
        format="DD MMM YYYY"
        showTime={true}
        value={!value ? null : new Date(value)}
      />
      {touched && error ? <span>{error}</span> : false}
    </div>
  );
};

class HomeFilterForm extends Component {
  state = {
    date: new Date(),
  };
  render() {
    return (
      <div>
        <Form>
          <div className="search-bar-container">
            <div className="search-placeholder">Search</div>
            <Field name="search" component={renderSearch} />
          </div>
          <div className="filters">
            <Row>
              <Col xs={6}>
                <Field
                  name="date"
                  showTime={false}
                  component={renderDateTimePicker}
                />
              </Col>
              <Col xs={6}>
                <Field name="league" component={renderDropdown} />
              </Col>
            </Row>
            <Row>
              <Col xs={6}>
                {this.props.filter && (
                  <Button
                    onClick={this.props.onClearFiltersClick}
                    block
                    style={{ marginTop: "20px" }}
                    variant="danger"
                  >
                    <FaBackspace /> Clear Filters
                  </Button>
                )}
              </Col>
              <Col xs={6}>
                {this.props.filterForm && this.props.filterForm.values && (
                  <button
                    onClick={(e) => {
                      e.preventDefault();
                      this.props.onSearchClick();
                    }}
                    className="my-btn"
                    style={{ marginTop: "20px", width: "100%" }}
                  >
                    <FaSearch /> Search
                  </button>
                )}
              </Col>
            </Row>
          </div>
        </Form>
      </div>
    );
  }
}

const mapStateToProps = (store) => {
  return {
    filterForm: store.form.FilterForm,
  };
};

export default reduxForm({
  form: "FilterForm",
})(connect(mapStateToProps, {})(HomeFilterForm));
