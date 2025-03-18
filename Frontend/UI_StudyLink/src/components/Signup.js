import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Auth from './Auth';
import { useDispatch } from 'react-redux';
import { login } from '../redux/features/loginSlice';
import './Signup.css';

function Signup() {
  const navigate = useNavigate();
  const apiBase = process.env.REACT_APP_API_BASE;
  const dispatch = useDispatch();
  const [formData, setFormData] = useState({});

  useEffect(() => {
    const googleData = sessionStorage.getItem('googleAuthData');
    if (googleData) {
      const parsedData = JSON.parse(googleData);
      setFormData({
        email: parsedData.email,
        name: parsedData.name,
        picture: parsedData.picture,
        googleId: parsedData.googleId,
        credentials: parsedData.credentials
      });
      sessionStorage.removeItem('googleAuthData');
    }
    else {
      navigate('/login');
    }
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('formData', formData)
    try {
      const response = await fetch(`${apiBase}/users/${formData.email.split('@')[0]}/profile?token=${formData.token}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Google-Token': `${formData.credentials}`,
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const fullData = {
        ...formData,
        ...data[0].profile
      };
      dispatch(login(fullData));
      localStorage.setItem('user', JSON.stringify(fullData));

      navigate('/study-groups');
    } catch (error) {
      console.error('Error during signup:', error);
      alert('Failed to sign up. Please try again.');
    }
  };

  return (
    <div className="signup-container">
      <div className="signup-box">
        <h2>Sign Up</h2>
        <form className="signup-form" onSubmit={handleSubmit}>
          <input
            type="password"
            name="token"
            placeholder="Courseworks Token"
            value={formData.token}
            onChange={handleChange}
            required
          />
          <button type="submit">Sign Up</button>
        </form>
      </div>
    </div>
  );
}

export default Signup; 