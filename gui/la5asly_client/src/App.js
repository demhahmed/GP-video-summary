import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { connect } from "react-redux";

import Home from "./components/Home";
import NotFound from "./components/NotFound";
import SignIn from "./components/SignIn";
import Navigation from "./components/Navigation";
import SignUp from "./components/SignUp/SignUp";
import Summaries from "./components/Summaries";
import UploadMatch from "./components/UploadMatch";
import Notification from "./components/Notification";
import SummaryDetails from "./components/SummaryDetails";

import { fetchUser } from "./actions";
import "./App.css";

class App extends React.Component {
  componentDidMount() {
    this.props.fetchUser();
  }

  render() {
    return (
      <div className="app">
        <Router>
          <div className="page-wrap">
            <Switch>
              <Route path="/signup" component={signUpContainer} exact />
              <Route component={defaultContainer} />
            </Switch>
          </div>
        </Router>
        <Notification />
      </div>
    );
  }
}

const defaultContainer = () => {
  return (
    <div>
      <Navigation />
      <Switch>
        <Route path="/" component={Home} exact />
        <Route path="/uploadmatch" component={UploadMatch} exact />
        <Route path="/summary_details/:id" component={SummaryDetails} exact />
        <Route component={NotFound} />
      </Switch>
    </div>
  );
};

const signUpContainer = () => {
  return (
    <div>
      <Switch>
        <Route path="/" component={Home} exact />
        <Route path="/signup" component={SignUp} exact />
        <Route component={NotFound} />
      </Switch>
    </div>
  );
};

const mapStateToProps = (store) => {
  return { user: store.user };
};

export default connect(mapStateToProps, { fetchUser })(App);
