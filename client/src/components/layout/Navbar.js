import React, { Component } from "react";
import { Link } from "react-router-dom";
import { logoutUser } from "../../actions/authActions";
import { connect } from "react-redux";
import PropTypes from "prop-types";

export class Navbar extends Component {
  onLogoutClick = e => {
    
    //e.preventDefault();
    this.props.logoutUser();
  };

  render() {
    return (
      <div className="navbar-fixed">
        <nav className="z-depth-0">
          
          <div className="nav-wrapper white">
            <Link
              to="/"
              style={{ fontFamily: "monospace" }}
              className="col s5 brand-logo center black-text"
            >
              <i className="material-icons">code</i>
              FASTBOT
            </Link>
            <div>
            <button
              style={{
                width: "110px",
                borderRadius: "12px",
                letterSpacing: "1px",
                marginTop: "1rem",
                marginRight:"1760px"
              }}
              onClick={() => {
                  this.onLogoutClick();
              }}
              className="btn btn-large black accent-2 white-text"
            >
              Logout
            </button>
            </div>
            </div>
        </nav>
      </div>
    );
  
  }
  
}

Navbar.propTypes = {
  logoutUser: PropTypes.func.isRequired,
  auth: PropTypes.object.isRequired
};

const mapStateToProps = state => ({
  auth: state.auth
});

export default connect(
  mapStateToProps,
  { logoutUser }
)(Navbar);