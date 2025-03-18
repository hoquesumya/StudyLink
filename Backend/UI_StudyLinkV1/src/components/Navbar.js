import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { logout } from '../redux/features/loginSlice';
import { useEffect } from 'react';
import './Navbar.css';

function Navbar() {
  const isLoggedIn = useSelector((state) => state.login.isLoggedIn);
  const loggedUser = useSelector(state => state.login.loggedUser) || JSON.parse(localStorage.getItem('user'));
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const apiBase = process.env.REACT_APP_API_BASE;


  const handleLogout = async () => {
    try {
      if (window.google?.accounts) {
        google.accounts.id.cancel();
        google.accounts.id.disableAutoSelect();
      }
      dispatch(logout());
      navigate('/');
    } catch (error) {
      console.error('Error during logout:', error);
      dispatch(logout());
      navigate('/');
    }
  };

  const handleDeleteAccount = async (e) => {
    e.preventDefault();
  
    if (window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      try {
        const response = await fetch(`${apiBase}/users/${loggedUser.user_id}/profile`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${loggedUser.jwt_token}`,
            'Google-Token': `${loggedUser.credentials}`
          },
        });
  
        if (response.ok) {
          console.log('Account successfully deleted');
          dispatch(logout());
          navigate('/');
        } else {
          console.error('Failed to delete account:', response.statusText);
        }
      } catch (error) {
        console.error('Error deleting account:', error);
        alert('Error deleting account. Please try again later.');
      }
    }
  };

  return (
    <nav className="navbar">
      <ul className="nav-links">
        <li><Link to="/">Home</Link></li>
        {isLoggedIn && (
          <>
            <li><Link to="/messages">Messages</Link></li>
            <li><Link to="/calendar">Calendar</Link></li>
            <li><Link to="/study-groups">Study Groups</Link></li>
          </>
        )}
      </ul>
      <div className="auth-button">
        {isLoggedIn ? (
          <>
            <Link to="/" onClick={handleLogout} className="btn btn-primary">Logout</Link>
            <Link 
              to="/" 
              onClick={handleDeleteAccount} 
              className="btn btn-danger" 
              style={{ marginLeft: '10px' }}
            >
              Delete Account
            </Link>
          </>
        ) : (
          <>
            <Link to="/login" className="btn btn-primary">Login</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
