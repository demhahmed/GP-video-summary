import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { connect } from "react-redux";

import Home from "./components/Home";
import NotFound from "./components/NotFound";
import SignIn from "./components/SignIn";
import Navigation from "./components/Navigation";
import SignUp from "./components/SignUp/SignUp";
import UploadMatch from "./components/UploadMatch";
import Notification from "./components/Notification";
import SummaryDetails from "./components/SummaryDetails";

import { prepareData } from "./actions";
import Footer from "./components/Footer";
import Loading from "./components/Loading";
import About from "./components/About";

class App extends React.Component {
  async componentWillMount() {
    await this.props.prepareData()
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
        <Footer />
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
        <Route path="/about" component={About} exact />
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

export default connect(mapStateToProps, { prepareData })(App);
