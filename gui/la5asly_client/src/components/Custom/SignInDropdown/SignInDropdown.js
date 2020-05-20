import React, { Component } from "react";
import {
  Button,
  Form,
  Row,
  Col,
  Image,
  Dropdown,
  FormControl,
} from "react-bootstrap";
import { Field, reduxForm } from "redux-form";
import { FaGoogle } from "react-icons/fa";
import validator from "validator";
import googleLogo from "../../../assets/google.svg";
import "./SignInDropdown.css";

const renderField = ({
  input,
  label,
  placeholder,
  type,
  meta: { touched, error },
}) => {
  return (
    <div>
      <p className="my-label">{label}</p>
      <div>
        <input
          className="signin-custom-input"
          {...input}
          type={type}
          placeholder={placeholder}
          type="text"
        />
      </div>
      {touched && error && <span className="error-msg">{error}</span>}
    </div>
  );
};

class SignInDropdown extends Component {
  state = {
    value: "",
  };

  CustomToggle = React.forwardRef(({ children, onClick }, ref) => (
    <button onClick={(e) => onClick(e)} ref={ref} className="my-btn">
      {children}
    </button>
  ));

  CustomMenu = React.forwardRef(({ className }, ref) => {
    return (
      <div ref={ref} className={className}>
        <Form autoComplete="off" onClick={(e) => e.preventDefault()}>
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
        <Row>
          <Col xs={6}>
            <button className="my-btn dropdown-mybtn">Sign Up</button>
          </Col>
          <Col xs={6}>
            <button className="my-btn dropdown-mybtn">Sign In</button>
          </Col>
        </Row>
        <button className="google-btn btn">
          <FaGoogle /> Sign in with google
        </button>
      </div>
    );
  });

  render() {
    return (
      <Dropdown>
        <Dropdown.Toggle as={this.CustomToggle} id="dropdown-custom-components">
          Sign In
        </Dropdown.Toggle>
        <Dropdown.Menu
          className="custom-dropdown"
          as={this.CustomMenu}
        ></Dropdown.Menu>
      </Dropdown>
    );
  }
}

const validate = (formValues) => {
  const errors = {};
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
  form: "signIn",
  validate,
})(SignInDropdown);
