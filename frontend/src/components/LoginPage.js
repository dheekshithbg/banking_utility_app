import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

// Define the base URL once
const API_BASE_URL = 'http://localhost:5000';

// Define the hardcoded admin credentials
const ADMIN_USERNAME = 'admin';
const ADMIN_PASSWORD = 'admin123';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // --- NEW ADMIN CHECK LOGIC ---
    if (username === ADMIN_USERNAME && password === ADMIN_PASSWORD) {
      // 1. If credentials match admin, skip API call and navigate directly
      setLoading(false);
      navigate('/admin');
      return;
    }
    // -----------------------------

    try {
      // 2. Proceed with regular user login API call
      const response = await axios.post(`${API_BASE_URL}/api/auth/login`, {
        username,
        password,
      });

      if (response.status === 200) {
        // Extract and Store the JWT Token AND user_id
        const { token, user_id } = response.data;
        
        localStorage.setItem('authToken', token); 
        localStorage.setItem('currentUserId', user_id); 
        
        navigate('/home');
      }
    } catch (err) {
      // 3. Handle regular login errors
      let errorMessage = 'Login failed. Please check your network connection.';

      if (err.response) {
        // Use the specific message provided by your Flask backend (400 or 401)
        if (err.response.data && err.response.data.message) {
          errorMessage = err.response.data.message; 
        } else if (err.response.status === 401 || err.response.status === 400) {
          // Fallback message for invalid user/pass
          errorMessage = 'Invalid username or password. Please try again.';
        } else if (err.response.status === 404) {
          errorMessage = 'Login endpoint not found. Check server URL.';
        } else {
          errorMessage = 'Username and password are required.';
        }
      } 
      
      setError(errorMessage);
    } finally {
        setLoading(false);
    }
  };

  return (
    <div className="login-page-wrapper">
      {/* Full-screen Background */}
      <div className="login-background"></div>

      {/* Login Card */}
      <div className="login-card">
        <div className="login-header">
          <h1>A One Way Place to pay for Utility Payments</h1>
          <p>Welcome back! Please login to continue</p>
        </div>

        {error && <div className="error-alert">{error}</div>}

        <form onSubmit={handleLogin} className="login-form">
          <input
            type="text"
            placeholder="Enter your username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            disabled={loading}
          />
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
          />
          <button type="submit" className="login-btn" disabled={loading}>
            {loading ? 'Logging In...' : 'Login Securely'}
          </button>
        </form>

        <p className="register-link">
          Don't have an account? <a href="/register">Register here</a>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;