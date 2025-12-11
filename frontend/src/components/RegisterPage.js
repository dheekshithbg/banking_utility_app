import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
const API_BASE_URL = 'http://localhost:5000';

function RegisterPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [phone_number, setPhoneNumber] = useState('');
  const [pan, setPan] = useState('');
  const [aadhaar, setAadhaar] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const payload = {
        username,
        password,
        email,
        phone_number,
        pan,
        aadhaar,
      };

      // POST to backend register endpoint. Assumes frontend proxy is configured
      // or backend is reachable at the same origin under /api.
      const response = await axios.post(`${API_BASE_URL}/api/auth/register`, payload);

      // Successful creation: backend may return 200 or 201
      if (response.status === 200 || response.status === 201) {
        alert('Registration successful! Please login.');
        navigate('/login');
        return;
      }

      // If backend returns a non-2xx but no exception thrown, show message
      const message = (response.data && response.data.message) || 'Registration failed. Please check your data.';
      setError(message);
      alert(`Registration error: ${message}`);
    } catch (err) {
      // Prefer detailed backend message when available
      let message = 'Registration failed. Please try again later.';
      if (err.response && err.response.data) {
        // common patterns: { message: '...' } or { errors: [...] }
        if (err.response.data.message) {
          message = err.response.data.message;
        } else if (err.response.data.errors) {
          try {
            message = Array.isArray(err.response.data.errors)
              ? err.response.data.errors.map(e => e.msg || e).join('; ')
              : String(err.response.data.errors);
          } catch (parseErr) {
            message = JSON.stringify(err.response.data.errors);
          }
        } else {
          message = JSON.stringify(err.response.data);
        }
      } else if (err.message) {
        message = err.message;
      }

      setError(message);
      alert(`Registration error: ${message}`);
      console.error('Registration error:', err);
    }
  };

  return (
    <div className="register-page-wrapper">
      {/* Full-screen Background - Same as Login */}
      <div className="register-background"></div>

      {/* Glassmorphism Register Card */}
      <div className="register-card">
        <div className="register-header">
          <h1>Create Account</h1>
          <p>Join Payment Platform and pay bills effortlessly</p>
        </div>

        {error && <div className="error-alert">{error}</div>}

        <form onSubmit={handleRegister} className="register-form">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Create Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Phone Number"
            value={phone_number}
            onChange={(e) => setPhoneNumber(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="PAN Number (e.g. ABCDE1234F)"
            value={pan}
            onChange={(e) => setPan(e.target.value.toUpperCase())}
            required
          />
          <input
            type="text"
            placeholder="Aadhaar Number (12 digits)"
            value={aadhaar}
            onChange={(e) => setAadhaar(e.target.value)}
            maxLength="12"
            required
          />

          <button type="submit" className="register-btn">
            Create Account
          </button>
        </form>

        <p className="login-link">
          Already have an account? <a href="/login">Login here</a>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;