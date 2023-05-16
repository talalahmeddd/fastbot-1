import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import jwt_decode from "jwt-decode"
import setAuthToken from "./utils/setAuthToken";
import { setCurrentUser, logoutUser } from "./actions/authActions";

import { Provider } from "react-redux";
import store from "./store";
import Register from "./components/auth/Register";
import Login from "./components/auth/Login";
import PrivateRoute from "./components/private-route/PrivateRoute";
import Dashboard from "./components/dashboard/Dashboard";
import SupportAdmin from './SupportAdmin';
import adminDash from "./components/adminDash/adminDash";
import AccuracyReport from "./components/reports/reports";
import './App.css'

// Check for token to keep user logged in
if(localStorage.jwtToken){
  // Set auth token header auth
  const token = localStorage.jwtToken
  setAuthToken(token)
  // Decode token and get user info and exp
  const decoded = jwt_decode(token)
  // Set user and isAuthenticated
  store.dispatch(setCurrentUser(decoded))

  // check for expired token
  const currentTime = Date.now() / 1000 // to get in millisecond
  if(decoded.exp < currentTime){
    // Logout user
    store.dispatch(logoutUser())

    // Redirect to login
    window.location.href = "./login"
  }
}

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <Router>
          <div className="App">
            {/* <Navbar /> */}
            <Route exact path="/" component={Login} />
            <Route exact path="/login" component={Login} />
            <Route exact path="/register" component={Register} />
            <Switch>
              <PrivateRoute exact path="/dashboard" component={Dashboard} />
              <PrivateRoute exact path="/adminDash" component={adminDash} />
              <PrivateRoute exact path="/support" component={SupportAdmin} />
              <PrivateRoute exact path="/report" component={AccuracyReport} />
           </Switch>
          </div>
        </Router>
      </Provider>
    );
  }
}

export default App;
