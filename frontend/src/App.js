import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import HomePage from './components/HomePage';
import PaymentSuccess from './components/PaymentSuccess';
import './App.css';
import AddServicePage from './components/AddServicePage';
import AdminPage from './components/Admin';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/payment-success" element={<PaymentSuccess />} />
        <Route path="/" element={<LoginPage />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/add_service" element={<AddServicePage />} />
      </Routes>
    </Router>
  );
}

export default App;
