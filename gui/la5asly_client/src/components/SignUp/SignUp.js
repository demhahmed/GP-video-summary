import React from "react";
import { Field, reduxForm } from "redux-form";
import { Button, Form, Row, Col } from "react-bootstrap";

import { IoLogoGoogle } from "react-icons/io";

import validator from "validator";
import "./SignUp.css";

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

class SignUp extends React.Component {
  handleSubmit = ({
    username,
    password,
    email,
    firstName,
    lastName,
    birthDate,
  }) => {
    this.props.handleSignUp(
      username,
      password,
      email,
      firstName,
      lastName,
      birthDate
    );
  };

  responseSuccessGoogle = (response) => console.log(response);
  responseFailGoogle = (response) => console.log(response);

  render() {
    return (
      <div className="my-form">
        <Row>
          <Col xs={{ offset: 3 }}>
            <h2 style={{ marginBottom: "30px" }}>Create a new account</h2>
          </Col>
        </Row>
        <Form onSubmit={this.props.handleSubmit(this.handleSubmit)}>
          <Field
            name="username"
            type="text"
            label="Username"
            placeholder="Enter Username"
            component={renderField}
          />
          <Field
            name="email"
            type="email"
            label="Email"
            placeholder="Enter Email"
            component={renderField}
          />

          <Field
            name="password"
            type="password"
            label="Password"
            placeholder="Enter Password"
            component={renderField}
          />
        </Form>
        <Form.Group as={Row}>
          <Col sm={{ offset: 3 }}>
            <div className="text-center">
              <Button block type="submit">
                Sign Up
              </Button>
            </div>
          </Col>
        </Form.Group>
        <Form.Group as={Row}>
          <Col sm={{ offset: 3 }}>
            <div className="text-center">
             
            </div>
          </Col>
        </Form.Group>
      </div>
    );
  }
}

const validate = (formValues) => {
  const errors = {};
  if (!formValues.username) {
    errors.username = "You must enter a username";
  }
  if (!formValues.password) {
    errors.password = "You must enter a password";
  }
  if (
    !formValues.email ||
    (formValues.email && !validator.isEmail(formValues.email))
  ) {
    errors.email = "You must enter a valid email";
  }
  return errors;
};

export default reduxForm({
  form: "signUpForm",
  validate,
})(SignUp);
