import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './components/Login';
import MessagingApp from './components/MessagingApp';
import CalendarPage from './components/CalendarPage';
import StudyGroups from './components/StudyGroups';
import Home from './components/Home';
import Signup from './components/Signup';
import { useSelector, useDispatch } from 'react-redux';
import { login } from './redux/features/loginSlice'; 
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';
import { logout } from './redux/features/loginSlice';
import { useNavigate } from 'react-router-dom';


function App() {
  const dispatch = useDispatch();
  const isLoggedIn = useSelector(state => state.login.isLoggedIn) || localStorage.getItem('user') !== null;
  const apiBase = process.env.REACT_APP_API_BASE;
  const ONE_SECOND = 1000;
  const ONE_MINUTE = ONE_SECOND * 60;     

  console.log('attempt 11')

  useEffect(() => {
    const checkUserSession = async () => {
      const user = localStorage.getItem('user');
      const userData = JSON.parse(user);
      const apiResponse = await fetch(`${apiBase}/users/${userData.email.split('@')[0]}/profile`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${userData.jwt_token}`,
          'Google-Token': `${userData.credentials}`
        }
      });
      if (apiResponse.status === 401) {
        sessionStorage.removeItem('googleAuthData');
        dispatch(logout());
        localStorage.removeItem('user');
        window.location.href = '/';
      }
      else {
        dispatch(login(userData));
        localStorage.setItem('user', JSON.stringify(userData));
      }
    } 
    checkUserSession();
  }, []); 

  return (
    <Router>
      <div className="app-container">
        <Navbar />
        <div className="content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/login" element={<Login />} />
            <Route
              path="/messages"
              element={
                <ProtectedRoute isLoggedIn={isLoggedIn}>
                  <MessagingApp />
                </ProtectedRoute>
              }
            />
            <Route
              path="/calendar"
              element={
                <ProtectedRoute isLoggedIn={isLoggedIn}>
                  <CalendarPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/study-groups"
              element={
                <ProtectedRoute isLoggedIn={isLoggedIn}>
                  <StudyGroups />
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}


export default App;
