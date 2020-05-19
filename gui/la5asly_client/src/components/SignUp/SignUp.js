import React from "react";
import { Field, reduxForm } from "redux-form";
import { Button, Form, Row, Col, Image } from "react-bootstrap";

import { FaHome } from "react-icons/fa";

import logo from "../../assets/logo_svg.svg";
import signup_image from "../../assets/sign in.jpg";

import validator from "validator";
import TooltipError from "../Custom/TooltipError";
import "./SignUp.css";

const renderField = ({
  input,
  label,
  placeholder,
  type,
  meta: { touched, error },
}) => {
  return (
    <div className="input-container">
      <p className="label">{label}</p>
      <div className="input-tooltip-container">
        <input
          className="custom-input"
          {...input}
          type={type}
          placeholder={placeholder}
          type="text"
        />
        {touched && error && (
          <TooltipError className="tooltip-pos" error_msg={error} />
        )}
      </div>
    </div>
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
      <div>
        <div className="back-home">
          <FaHome /> Back to Home
        </div>
        <Image className="bk-overlay" src={signup_image} />
        <div className="dark-overlay" />
        <Image src={logo} className="logo" />
        <div className="my-form">
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
          <div className="buttons">
            <button className="custom-btn" type="submit">
              Sign Up
            </button>
          </div>
        </div>
      </div>
    );
  }
}

const validate = (formValues) => {
  const errors = {};
  if (!formValues.username) {
    errors.username = "Invalid username";
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
