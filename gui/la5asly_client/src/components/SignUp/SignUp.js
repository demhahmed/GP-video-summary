import React from "react";
import { Field, reduxForm } from "redux-form";
import { Button, Form, Row, Col, Image } from "react-bootstrap";

import { FaHome } from "react-icons/fa";

import logo from "../../assets/logo_svg.svg";
import signup_image from "../../assets/sign in.jpg";

import validator from "validator";
import TooltipError from "../Custom/TooltipError";
import "./SignUp.css";
import { Link, Redirect } from "react-router-dom";
import FileUpload from "../FileUploader/FileUpload";
import { connect } from "react-redux";
import { signUp, fetchUser } from "../../actions";

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
        />
        {touched && error && (
          <TooltipError className="tooltip-pos" error_msg={error} />
        )}
      </div>
    </div>
  );
};

class SignUp extends React.Component {
  state = { img: null, imgObj: null };

  handleSubmit = () => {
    this.props.signUp(
      this.props.signUpForm.values.email,
      this.props.signUpForm.values.password,
      this.state.imgObj
    );
  };
  responseSuccessGoogle = (response) => console.log(response);
  responseFailGoogle = (response) => console.log(response);
  onFileSelected = (img) => {
    this.setState({ img: URL.createObjectURL(img), imgObj: img });
  };
  render() {
    if (this.props.user.isLoggedIn) {
      this.props.fetchUser();
      return <Redirect to="/" />;
    }
    const activeBtn =
      this.props.signUpForm &&
      !this.props.signUpForm.syncErrors &&
      this.state.img;
    return (
      <div className="container">
        <Link className="custom-link" to="/">
          <div className="back-home">
            <FaHome /> Back to Home
          </div>
        </Link>
        <Image className="bk-overlay" src={signup_image} />
        <div className="dark-overlay" />
        <Image src={logo} className="logo" />
        <div className="my-form">
          <Form onSubmit={this.props.handleSubmit(this.handleSubmit)}>
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
          <div style={{ marginTop: "20px" }} className="input-container">
            <p className="label">Image</p>
            <FileUpload
              onFileSelected={this.onFileSelected}
              style={{ color: "#777474", border: "1px solid #dd4b00" }}
            />
            {this.state.img && (
              <Image className="preview-img" src={this.state.img} />
            )}
          </div>
          <div className={`buttons`}>
            <button
              onClick={() => {
                if (activeBtn) this.handleSubmit();
              }}
              className={`custom-btn  ${activeBtn ? "" : "disabled-btn"}`}
              type="submit"
            >
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

const mapStateToProps = (store) => {
  return {
    signUpForm: store.form.signUpForm,
    user: store.user,
  };
};

export default reduxForm({
  form: "signUpForm",
  validate,
})(connect(mapStateToProps, { signUp, fetchUser })(SignUp));
