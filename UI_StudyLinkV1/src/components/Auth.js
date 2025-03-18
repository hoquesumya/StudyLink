import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { login, logout } from '../redux/features/loginSlice';

function Auth() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const apiBase = process.env.REACT_APP_API_BASE;


  const SESSION_DURATION = 10 * 60 * 1000; 

  useEffect(() => {
    google.accounts.id.initialize({
      client_id: process.env.REACT_APP_GOOGLE_CLIENT_ID,
      callback: handleCredentialResponse,
      auto_select: false,
      prompt_parent_id: "google-signin-button"
    });

    google.accounts.id.renderButton(
      document.getElementById("google-signin-button"),
      { 
        theme: "outline", 
        size: "large",
        type: "standard",
        prompt_parent_id: "google-signin-button"
      }
    );
  }, []);

  const handleCredentialResponse = async (response) => {
    try {
      const decodedToken = JSON.parse(atob(response.credential.split('.')[1]));
      console.log("Decoded token:", decodedToken);
      console.log("Response:", response);
      const apiResponse = await fetch(`${apiBase}/users/${decodedToken.email.split('@')[0]}/login`, {
        method: 'GET',
        headers: {
          'Google-Token': `${response.credential}`
        }
      });
  
      if (!apiResponse.ok) {
        const wantToSignup = window.confirm(
          "No user profile exists for this Google account. Would you like to create one?"
        );
        
        if (wantToSignup) {
          sessionStorage.setItem('googleAuthData', JSON.stringify({
            email: decodedToken.email,
            name: decodedToken.name,
            picture: decodedToken.picture,
            googleId: decodedToken.sub,
            credentials: response.credential
          }));
          
          navigate('/signup');
        }
        return;
      }

      if (!apiResponse.ok) {
        throw new Error(`HTTP error! status: ${apiResponse.status}`);
      }

      const userData = await apiResponse.json();
      console.log("User data:", userData);
      
      const completeUserData = {
        ...userData,
        googleId: decodedToken.sub,
        name: decodedToken.name,
        email: decodedToken.email,
        picture: decodedToken.picture,
        loginTime: new Date().toISOString(),
        credentials: response.credential
      };

      dispatch(login(completeUserData));
      
      localStorage.setItem('user', JSON.stringify(completeUserData));

      setTimeout(() => {
        if (window.google?.accounts) {
          google.accounts.id.revoke(completeUserData.email, () => {
            console.log('Session expired - Google consent revoked');
          });
        }
        localStorage.removeItem('user');
        dispatch(logout());
        navigate('/');
        alert('Your session has expired. Please log in again.');
      }, SESSION_DURATION);

      navigate('/study-groups');
    } catch (error) {
      console.error('Error in handleCredentialResponse:', error);
      alert('An error occurred during login. Please try again.');
    }
  };

  return (
    <div className="auth-container">
      <div id="google-signin-button"></div>
    </div>
  );
}

export default Auth;