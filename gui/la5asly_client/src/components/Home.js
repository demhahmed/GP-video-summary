import React, { Component } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";

import { showNotification, hideNotification } from "../actions";

import Summaries from "./Summaries";

class Home extends Component {
  render() {
    return (
      <div className="bg-white">
        <Summaries />
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
