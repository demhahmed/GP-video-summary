import React, { Component } from "react";
import { connect } from "react-redux";
import { Field, reduxForm } from "redux-form";
import { Redirect } from "react-router-dom";
import { Button, Form, Row, Col } from "react-bootstrap";
import DropdownList from "react-widgets/lib/DropdownList";
import moment from "moment";
import momentLocaliser from "react-widgets-moment";
import { showNotification, hideNotification, summarize } from "../../actions";

import "react-widgets/dist/css/react-widgets.css";

momentLocaliser(moment);

const renderField = ({
  input,
  label,
  placeholder,
  type,
  meta: { touched, error },
}) => {
  return (
    <Form.Group as={Row} controlId="formHorizontalEmail">
      <Form.Label column sm={3}>
        {label}
      </Form.Label>
      <Col sm={9}>
        <Form.Control {...input} type={type} placeholder={placeholder} />
        {touched && error && <span className="text-danger">{error}</span>}
      </Col>
    </Form.Group>
  );
};

class UploadMatch extends React.Component {
  state = {
    error: null,
  };
  leagues = [
    { league: "Premier League", value: "PREMIER_LEAGUE" },
    { league: "La Liga", value: "LA_LIGA" },
    { league: "Ligue 1", value: "LIGUE_1" },
    { league: "BundesLiga", value: "BUNDESLIGA" },
  ];

  handleSubmit = ({ title, leagueType }) => {
    if (this.state.file) {
      this.props.summarize(this.props.user._id, title, leagueType, this.state.file)
    } else {
      this.setState({ error: true });
    }
  };

  renderDropdownList = ({ input, data, valueField, textField }) => {
    return (
      <DropdownList
        {...input}
        data={data}
        valueField={valueField}
        textField={textField}
        onChange={input.onChange}
      />
    );
  };

  render() {
    if (!this.props.user) {
      this.props.showNotification("You are not logged in to upload summary!");
      setTimeout(() => {
        this.props.hideNotification();
      }, 2000);
      return <Redirect to="/" />;
    }
    return (
      <div className="my-form">
        <Row>
          <Col xs={{ offset: 3 }}>
            <h2 style={{ marginBottom: "30px" }}>Summarize a new match</h2>
          </Col>
        </Row>
        <Form onSubmit={this.props.handleSubmit(this.handleSubmit)}>
          <Field
            name="title"
            type="text"
            label="Title"
            placeholder="Enter title"
            component={renderField}
          />

          <Row style={{ marginBottom: "15px" }}>
            <Form.Label column sm={3}>
              League Type
            </Form.Label>
            <Col sm={9}>
              <Field
                name="leagueType"
                component={this.renderDropdownList}
                data={this.leagues}
                valueField="value"
                textField="league"
              />
            </Col>
          </Row>
          <Form.Group as={Row}>
            <Form.Label column sm={3}>
              Match File
            </Form.Label>
            <Col sm={9}>
              <input
                type="file"
                onChange={(e) => {
                  this.setState({ file: e.target.files, error: null });
                }}
              />
              {this.state.error && (
                <p className="text-danger">please upload a file</p>
              )}
            </Col>
          </Form.Group>
          <Form.Group as={Row}>
            <Col sm={{ offset: 3 }}>
              <Button block variant="success" type="submit">
                Summarize
              </Button>
            </Col>
          </Form.Group>
        </Form>
      </div>
    );
  }
}

const validate = (formValues) => {
  const errors = {};
  if (!formValues.title) {
    errors.title = "You must enter a title";
  }
  if (!formValues.leagueType) {
    errors.leagueType = "You must enter a leagueType";
  }
  return errors;
};

const mapStateToProps = (store) => {
  return { user: store.user.user };
};

export default connect(mapStateToProps, { showNotification, hideNotification, summarize })(
  reduxForm({
    form: "uploadMatch",
    validate,
  })(UploadMatch)
);
