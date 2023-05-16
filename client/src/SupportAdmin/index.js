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
      projectID={"bffa24af-7c93-4675-a976-0bf84d466b63"}
      userName='FastBot'
      userSecret='Fastbot@123'
      height='calc(100vh - 12px)'
    />
    </div>
  );
}
export default SupportAdmin;
