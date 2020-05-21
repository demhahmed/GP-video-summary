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
import { Link } from "react-router-dom";
import { connect } from "react-redux";
import { signIn } from "../../../actions";

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

  handleSubmit = () => {
    const { email, password } = this.props.signInForm.values;
    this.props.signIn(email, password);
  };

  CustomToggle = React.forwardRef(({ children, onClick }, ref) => (
    <button onClick={(e) => onClick(e)} ref={ref} className="my-btn">
      {children}
    </button>
  ));

  CustomMenu = React.forwardRef(({ className }, ref) => {
    const activeBtn =
      this.props.signInForm && !this.props.signInForm.syncErrors;
    console.log(activeBtn);
    return (
      <div ref={ref} className={className}>
        <Form onClick={(e) => e.preventDefault()}>
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
            <Link to="/signup" className="custom-link">
              <button className="my-btn dropdown-mybtn">Sign Up</button>
            </Link>
          </Col>
          <Col xs={6}>
            <button
              onClick={() => {
                if (activeBtn) this.handleSubmit();
              }}
              className={`my-btn dropdown-mybtn ${
                activeBtn ? "" : "disabled-btn"
              }`}
            >
              Sign In
            </button>
          </Col>
        </Row>
        <a className="custom-link" href="/auth/google">
          <button className="google-btn btn">
            <FaGoogle /> Sign in with google
          </button>
        </a>
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
  if (
    !formValues.password ||
    (formValues.password && formValues.password.length < 8)
  ) {
    errors.password = "You must enter a password, at least 8 characters";
  }
  if (
    !formValues.email ||
    (formValues.email && !validator.isEmail(formValues.email))
  ) {
    errors.email = "You must enter a valid email";
  }
  return errors;
};

const mapStateToProps = (store) => {
  return { signInForm: store.form.signInForm };
};

export default reduxForm({
  form: "signInForm",
  validate,
})(connect(mapStateToProps, { signIn })(SignInDropdown));
