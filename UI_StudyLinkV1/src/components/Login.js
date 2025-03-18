import React from 'react';
import Auth from './Auth';
import './Login.css';


function Login() {

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Login</h2>
        <div className="login-form">
          <Auth /> 
        </div>
      </div>
    </div>
  );
}

export default Login;
