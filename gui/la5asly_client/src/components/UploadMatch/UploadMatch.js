import React, { Component } from "react";
import { connect } from "react-redux";
import { Field, reduxForm } from "redux-form";
import { Redirect } from "react-router-dom";
import { Button, Form, Row, Col, Image } from "react-bootstrap";
import DropdownList from "react-widgets/lib/DropdownList";
import Multiselect from "react-widgets/lib/Multiselect";
import moment from "moment";
import momentLocaliser from "react-widgets-moment";
import { showNotification, hideNotification, summarize } from "../../actions";
import uploadLogo from "../../assets/upload.svg";

import "react-widgets/dist/css/react-widgets.css";
import "./UploadMatch.css";
import Loading from "../Loading";
import FileUpload from "../FileUploader/FileUpload";
import uploadImage from "../../assets/upload.jpg";
import LeagueDropdown from "../Custom/LeagueDropdown/LeagueDropdown";
import TeamsDropdown from "../Custom/TeamsDropdown";
import { SelectList } from "react-widgets";
import { FaUpload } from "react-icons/fa";
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

const renderMultiselect = ({
  input,
  data,
  valueField,
  textField,
  meta: { touched, error },
}) => {
  return (
    <div>
      <Multiselect
        {...input}
        onBlur={() => input.onBlur()}
        value={input.value || []} // requires value to be an array
        data={data}
        valueField={valueField}
        textField={textField}
      />
      {touched && error && <span className="text-danger">{error}</span>}
    </div>
  );
};

class UploadMatch extends React.Component {
  state = {
    home: null,
    away: null,
    leagueId: null,
    versions: [],
    file: null,
  };

  onFileSelected = (file) => {
    this.setState({ file });
  };

  handleLeagueSelect = (leagueId) => {
    this.setState({ leagueId });
  };
  handleSubmit = () => {
    const { home, away, leagueId, versions, file } = this.state;
    this.props.summarize(
      this.props.user._id,
      leagueId,
      home,
      away,
      file,
      versions
    );
  };

  handleTeamSelect = (type, team) => {
    this.setState({ [type]: team });
  };

  handleVersionSelect = (version) => {
    let idx = this.state.versions.indexOf(version);
    if (idx !== -1) {
      this.setState({
        versions: this.state.versions.filter((version) => version !== version),
      });
    } else {
      this.setState({
        versions: [...this.state.versions, version],
      });
    }
  };

  render() {
    if (this.props.globalReducer.wait) {
      return <Loading />;
    }
    if (
      !this.props.user.isLoggedIn ||
      (this.props.user.isLoggedIn && this.props.user.type !== "admin")
    ) {
      this.props.showNotification(
        "You are not logged in as admin to upload video!"
      );
      setTimeout(() => {
        this.props.hideNotification();
      }, 2000);
      return <Redirect to="/" />;
    }
    const { home, away, leagueId, versions, file } = this.state;
    const activeBtn = home && away && leagueId && versions.length > 0 && file;

    return (
      <div className="container">
        <div className="my-form">
          <Image className="bk-overlay" src={uploadImage} />
          <div className="dark-overlay" />
          <section>
            <div className="home-header">
              <span>Upload</span>
            </div>
          </section>
          <p>Video Path</p>
          <div className="search-path">
            <FileUpload onFileSelected={this.onFileSelected} />
          </div>
          <p>League</p>
          <div className="league-drop-down">
            <LeagueDropdown
              handleLeagueSelect={this.handleLeagueSelect}
              className="smaller-dropdown"
            />
          </div>
          <section style={{ marginTop: "30px" }}>
            {this.props.leagues && this.state.leagueId && (
              <Row style={{ marginBottom: "20px" }}>
                <Col xs={4}>
                  <div className="league-drop-down">
                    <p>Home Team</p>
                    <TeamsDropdown
                      handleTeamSelect={(team) =>
                        this.handleTeamSelect("home", team)
                      }
                      leagueId={this.state.leagueId}
                    />
                  </div>
                </Col>
                <Col>
                  <div className="league-drop-down">
                    <p>Away Team</p>
                    <TeamsDropdown
                      handleTeamSelect={(team) =>
                        this.handleTeamSelect("away", team)
                      }
                      leagueId={this.state.leagueId}
                    />
                  </div>
                </Col>
              </Row>
            )}
          </section>
          <section>
            <p style={{ paddingTop: "45px" }}>Select Version</p>
            <button
              style={{ width: "100px" }}
              onClick={() => this.handleVersionSelect("detailed")}
              className={`my-btn ${
                this.state.versions.indexOf("detailed") === -1 ? "disabled" : ""
              }`}
            >
              Detailed
            </button>
            <button
              style={{ width: "100px" }}
              onClick={() => this.handleVersionSelect("audio")}
              className={`my-btn ${
                this.state.versions.indexOf("audio") === -1 ? "disabled" : ""
              }`}
            >
              Audio
            </button>
          </section>
          <section style={{ marginTop: "25px" }}>
            <button
              style={{ display: "inline-block" }}
              onClick={this.handleSubmit}
              className={`my-btn ${activeBtn ? "" : "disabled-btn"}`}
            >
              <FaUpload /> <span>Upload</span>
            </button>
          </section>
        </div>
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
  if (
    !formValues.versions ||
    (formValues.versions && formValues.versions.length === 0)
  ) {
    errors.versions = "You must select a verison";
  }
  return errors;
};

const mapStateToProps = (store) => {
  return {
    user: store.user,
    uploadMatchForm: store.form.uploadMatch,
    globalReducer: store.globalReducer,
    leagues: store.teams.leagues,
  };
};

export default connect(mapStateToProps, {
  showNotification,
  hideNotification,
  summarize,
})(
  reduxForm({
    form: "uploadMatch",
    validate,
  })(UploadMatch)
);
