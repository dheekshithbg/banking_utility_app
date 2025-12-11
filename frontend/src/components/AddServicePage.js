import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

function AddServicePage() {
  // State variables for BOTH Utility and Bill details
  const [name, setName] = useState(''); // Utility: name
  const [description, setDescription] = useState(''); // Utility: description
  const [provider_name, setProviderName] = useState(''); // Utility: provider_name
  const [amount, setAmount] = useState(''); // Bill: amount
  const [due_date, setDueDate] = useState(''); // Bill: due_date
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // ⚠️ NOTE: The user_id is crucial for the 'bills' table. 
  // In a real app, this should come from your global state, Redux store, 
  // or a context after the user has logged in. 
  // Using a hardcoded placeholder for this example:
  const USER_ID = 1; 

  const handleAddUtilityAndBill = async (e) => {
    e.preventDefault();
    setError('');

    if (!name || !provider_name || !amount || !due_date) {
      setError('Service Name, Provider, Bill Amount, and Due Date are required.');
      return;
    }

    try {
      // --- STEP 1: Add the Utility Service ---
      const utilityPayload = {
        name,
        description,
        provider_name,
      };

      // POST utility data to the backend (e.g., /api/utilities)
      const utilityResponse = await axios.post(`${API_BASE_URL}/api/utilities`, utilityPayload);

      if (utilityResponse.status !== 200 && utilityResponse.status !== 201) {
          throw new Error('Failed to create Utility Service.');
      }
      
      // Assume the backend returns the newly created utility_id in the response data
      const utility_id = utilityResponse.data.utility_id; 
      
      if (!utility_id) {
          throw new Error('Utility created but no utility_id was returned by the server.');
      }
      
      // --- STEP 2: Add the Initial Bill with the new utility_id ---
      const billPayload = {
        user_id: USER_ID, // Use the authenticated user ID
        utility_id: utility_id, // Use the ID from the previous step
        amount: parseFloat(amount), // Ensure amount is a number
        due_date,
        // status and created_at should typically be set by the backend
      };

      // POST bill data to the backend (e.g., /api/bills)
      const billResponse = await axios.post(`${API_BASE_URL}/api/bills`, billPayload);
      
      if (billResponse.status !== 200 && billResponse.status !== 201) {
          throw new Error('Failed to create initial Bill.');
      }
      
      // --- Success Notification and Navigation ---
      alert(`Utility Service "${name}" and initial Bill added successfully!`);
      navigate('/home'); // Navigate to a success page or dashboard
      
    } catch (err) {
      // --- Error Handling Block ---
      let message = 'Operation failed. Please try again later.';
      if (err.response && err.response.data) {
        // Prefer detailed backend message
        message = err.response.data.message || JSON.stringify(err.response.data);
      } else if (err.message) {
        message = err.message;
      }

      setError(message);
      alert(`Error: ${message}`);
      console.error('Operation error:', err);
    }
  };

  return (
    <div className="register-page-wrapper">
      <div className="register-background"></div>

      {/* Glassmorphism Card */}
      <div className="register-card">
        <div className="register-header">
          <h1>Add New Service & Initial Bill</h1>
          <p>Define a new utility service and its first bill details.</p>
        </div>

        {error && <div className="error-alert">{error}</div>}

        <form onSubmit={handleAddUtilityAndBill} className="register-form">
          {/* UTILITY SERVICE DETAILS */}
          <h3>Service Details</h3>
          <input
            type="text"
            placeholder="Service Name (e.g., Water Bill)"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Provider Name (e.g., City Water Board)"
            value={provider_name}
            onChange={(e) => setProviderName(e.target.value)}
            required
          />
          <input
            placeholder="Service Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />

          {/* INITIAL BILL DETAILS */}
          <h3 style={{ marginTop: '20px' }}>Initial Bill Details</h3>
          <input
            type="number"
            placeholder="Bill Amount (e.g., 550.00)"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
            min="0.01"
            step="0.01"
          />
          <input
            type="date"
            placeholder="Due Date"
            value={due_date}
            onChange={(e) => setDueDate(e.target.value)}
            required
          />

          <button type="submit" className="register-btn">
            Add Service & Bill
          </button>
        </form>

        <p className="login-link">
          <a href="/home">Back to HomePage</a>
        </p>
      </div>
    </div>
  );
}

export default AddServicePage;