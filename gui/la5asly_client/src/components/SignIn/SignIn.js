import React from "react";
import { Field, reduxForm } from "redux-form";
import { Button, Form, Row, Col } from "react-bootstrap";
import "./SignIn.css";
import { Link } from "react-router-dom";
import { IoLogoGoogle } from "react-icons/io";
import GoogleLogin from "react-google-login";

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

class SignIn extends React.Component {
  handleSubmit = (formValues) => {
    this.props.handleSignIn(formValues.username, formValues.password);
  };
  responseSuccessGoogle = (response) => console.log(response);
  responseFailGoogle = (response) => console.log(response);

  render() {
    return (
      <div className="my-form">
        <Row>
          <Col xs={{ offset: 3 }}>
            <h2 style={{ marginBottom: "30px" }}>
              Log in to <strong>La5asly</strong>
            </h2>
          </Col>
        </Row>
        <Form onSubmit={this.props.handleSubmit(this.handleSubmit)}>
          <Field
            name="username"
            type="text"
            label="Email/Username"
            placeholder="Enter Email / Username"
            component={renderField}
          />
          <Field
            name="password"
            type="password"
            label="Password"
            placeholder="Enter Password"
            component={renderField}
          />
          <Row>
            <Col xs={{ offset: 3 }}>
              <Row>
                <Col xs={6}>
                  <Button
                    className="sign-in-btn btn-block"
                    variant="primary"
                    type="submit"
                  >
                    Sign In
                  </Button>
                </Col>
                <Col xs={6}>
                  <Link className="custom-link" to="/signup">
                    <Button className="sign-in-btn btn-block" variant="success">
                      Sign Up
                    </Button>
                  </Link>
                </Col>
              </Row>
            </Col>
          </Row>
          <Row>
            <Col xs={{ offset: 3 }}>
              <div className="google-btn">
                <GoogleLogin
                  clientId="1024627819936-egebh5n0541fciddrtkrdnc8q3ju1snk.apps.googleusercontent.com"
                  buttonText="Login"
                  render={(renderProps) => (
                    <Button
                      {...renderProps}
                      block
                      type="submit"
                      variant="danger"
                    >
                      <IoLogoGoogle /> Sign in with google
                    </Button>
                  )}
                  onSuccess={this.responseSuccessGoogle}
                  onFailure={this.responseFailGoogle}
                  isSignedIn={true}
                />
              </div>
            </Col>
          </Row>
        </Form>
      </div>
    );
  }
}

const validate = (formValues) => {
  const errors = {};
  if (!formValues.username) {
    errors.username = "You must enter a username or password";
  }
  if (!formValues.password) {
    errors.password = "You must enter a password";
  }
  return errors;
};

export default reduxForm({
  form: "signInForm",
  validate,
})(SignIn);
