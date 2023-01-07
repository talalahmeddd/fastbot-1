import React, { Component } from "react";
import { Link } from "react-router-dom";
//import "./button.css"


class Navbar extends Component {
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
            </div>
            
            
            {/* <button 
              style={{
                width: "150px",
                borderRadius: "3px",
                letterSpacing: "1.5px",
                marginTop: "1rem",
                float: "right",
                color:"black",
                  
                
                
              }}
              
              className="btn"
            >
              Give Feedback
            </button> */}
            

        </nav>
      </div>
    );
  
  }
  
}

export default Navbar;
