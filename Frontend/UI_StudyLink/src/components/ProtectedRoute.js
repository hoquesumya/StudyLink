
import { useNavigate } from 'react-router-dom';
import { logout } from '../redux/features/loginSlice';
import { useDispatch } from 'react-redux';
import { useEffect } from 'react';

function ProtectedRoute({ children }) {
    const navigate = useNavigate();
    const dispatch = useDispatch();


    useEffect(() => {
      const checkSession = () => {
        const user = localStorage.getItem('user');
        if (user) {
          const userData = JSON.parse(user);
          const loginTime = new Date(userData.loginTime);
          const now = new Date();
          const sessionAge = now - loginTime;
  
          if (sessionAge >= 20 * 60 * 1000) {
            console.log("session expired");
            if (window.google?.accounts) {
              google.accounts.id.cancel();
              google.accounts.id.disableAutoSelect();
              google.accounts.id.revoke(userData.email, () => {
                console.log('Session expired - Google consent revoked');
              });
            }
            
            dispatch(logout());
            localStorage.removeItem('user');
            sessionStorage.removeItem('googleAuthData');
            
            alert('Your session has expired. Please log in again.');
            navigate('/login', { replace: true });
            
            return false; 
          }
          return true;
        }
        return false;
      };
  
      if (!checkSession()) {
        navigate('/login', { replace: true });
      }
  
      const interval = setInterval(checkSession, 30 * 1000);
      return () => clearInterval(interval);
    }, [dispatch, navigate]);
  
    const user = localStorage.getItem('user');
    return user ? children : null;
  }

export default ProtectedRoute;