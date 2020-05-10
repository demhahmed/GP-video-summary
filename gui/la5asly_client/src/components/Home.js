import React, { Component } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";

import { showNotification, hideNotification } from "../actions";

import Summaries from "./Summaries";

class Home extends Component {
  render() {
    if (this.props.myuploads && !this.props.user) {
      // NOT AUTHORIZED TO BE HERE.
      this.props.showNotification("You are not logged in to see your summaries!");
      setTimeout(() => {
        this.props.hideNotification();
      }, 2000);
      return <Redirect to="/" />;
    }
    return (
      <div className="bg-white">
        <Summaries myuploads={this.props.myuploads} />
      </div>
    );
  }
}

const mapStateToProps = (store) => {
  return { user: store.user.user };
};

export default connect(mapStateToProps, { showNotification, hideNotification })(
  Home
);
