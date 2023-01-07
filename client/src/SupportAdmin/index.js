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
      projectID={"8855f6b3-6587-4cde-9f9a-b09e21f90d3b"}
      userName='FAST BOT'
      userSecret='fastbot123'
      height='calc(100vh - 12px)'
    />
    </div>
  );
}
export default SupportAdmin;
