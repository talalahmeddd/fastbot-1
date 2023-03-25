import React, { Component } from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { logoutUser } from "../../actions/authActions";
import SupportEngine from '../../SupportEngine';
import FeedBack from 'react-feedback-popup';
import Navbar from "../layout/Navbar";



class Dashboard extends Component {
  render() {
    const { user } = this.props.auth;

    return (
      <div style={{backgroundColor:"black"}}>
        <Navbar/>
      <div style={{ height: "93.3vh" }} className="container valign-wrapper">
        <div className="row">
          <div className="landing-copy col s12 center-align white-text">
            <h4>
              <b>Hey there,</b> {user.name.split(" ")[0]}
              <p className="flow-text white-text text-darken-1">
                You are logged into {" "}
                <span style={{ fontFamily: "monospace" }}><b>FASTBOT</b></span>
              </p>
            </h4>
            <div className="col s12" style={{ paddingLeft: "11.250px" }}>
            <a href="http://127.0.0.1:5000/" target={"_blank"} rel="noreferrer">
            <button style={{
                    width: "200px",
                    borderRadius: "15px",
                    letterSpacing: "1.5px",
                    marginTop: "1rem",
                    marginLeft:"0px"
                  }}
                  type="submit"
                  className="btn btn-large white blue-text"
                >
                <b>CHATBOT</b>
            </button></a>
            </div>
            <div>
              <SupportEngine />
            </div>
            <div>
            <FeedBack
              
				style={{zIndex:'25', marginLeft:'20px'}}
				position="left"
				numberOfStars={5}
				headerText="Give Feedback"
				bodyText="Please provide feedback"
				buttonText="Feedback"
				handleClose={() => console.log("handleclose")}
				handleSubmit={(data) => 
					fetch('https://formspree.io/f/moqzqknr', {
						headers: {
							Accept: 'application/json',
							'Content-Type': 'application/json'
						},
						method: 'POST', // or 'PUT'
						body: JSON.stringify(data),
					}).then((response) => { 
						if (!response.ok) {
							return Promise.reject('Our servers are having issues! We couldn\'t send your feedback!');
						}
						response.json()
					}).then(() => {
						alert('Success!');
					}).catch((error) => {
						alert('Our servers are having issues! We couldn\'t send your feedback!', error);
					})
				}
				handleButtonClick={() => console.log("handleButtonClick")}/>
            </div>
          </div>
        </div>
      </div>
      </div>
    );
  }
}

Dashboard.propTypes = {
  logoutUser: PropTypes.func.isRequired,
  auth: PropTypes.object.isRequired
};

const mapStateToProps = state => ({
  auth: state.auth
});

export default connect(
  mapStateToProps,
  { logoutUser }
)(Dashboard);