import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import Home from "./components/Home";
import NotFound from "./components/NotFound";
import SignIn from "./components/SignIn";
import Navigation from "./components/Navigation";
import SignUp from "./components/SignUp/SignUp";
import Summaries from "./components/Summaries";
import UploadMatch from "./components/UploadMatch";
import SummaryDetails from "./components/SummaryDetails";

export default class App extends React.Component {
  render() {
    return (
      <div className=" App">
        <Router>
          <div>
            <Navigation />
            <Switch>
              <Route path="/" component={Home} exact />
              <Route path="/uploadmatch" component={UploadMatch} exact />
              <Route path="/summary_details/:id" component={SummaryDetails} exact />
              <Route component={NotFound} />
            </Switch>
          </div>
        </Router>
      </div>
    );
  }
}
