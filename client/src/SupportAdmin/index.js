import React from 'react';
import { Link } from "react-router-dom";

import { ChatEngine } from 'react-chat-engine'

const SupportAdmin = () => {
  return (
    <div>
      <Link to="/adminDash" className="btn-flat waves-effect">
              <i className="material-icons left">keyboard_backspace</i> Back to
              Admin Dashboard
            </Link>
    <ChatEngine 
      projectID={"110df2bc-720f-4402-82a6-4f6478d8b40c"}
      userName='FastBot'
      userSecret='fastbot123'
      height='calc(100vh - 12px)'
    />
    </div>
  );
}
export default SupportAdmin;
