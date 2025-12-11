import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // <-- NEW IMPORT
// import './AdminPage.css'; // Assuming you created this CSS file

const API_BASE_URL = 'http://localhost:5000'; // Match your backend port
const ADMIN_USERNAME = 'admin';
const ADMIN_PASSWORD = 'admin123'; 

function AdminPage() {
  const [activeTab, setActiveTab] = useState('users');
  const [data, setData] = useState({
    users: [],
    bills: [],
    payments: [],
    utilities: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // <-- Initialize navigate

  // --- NEW LOGOUT HANDLER ---
  const handleLogout = () => {
    // Admin login is client-side only, so we only need to redirect.
    // If you stored admin state (like a flag), you would clear it here.
    navigate('/login'); // Redirect back to the login page
  };
  // --------------------------

  useEffect(() => {
    // Configuration for Admin Basic Authentication (via custom headers)
    const authConfig = {
      headers: {
        'X-USERNAME': ADMIN_USERNAME,
        'X-PASSWORD': ADMIN_PASSWORD,
      },
    };

    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [usersRes, billsRes, paymentsRes, utilitiesRes] = await Promise.all([
          axios.get(`${API_BASE_URL}/api/admin/users`, authConfig),
          axios.get(`${API_BASE_URL}/api/admin/bills`, authConfig),
          axios.get(`${API_BASE_URL}/api/admin/payments`, authConfig),
          axios.get(`${API_BASE_URL}/api/admin/utilities`, authConfig),
        ]);

        setData({
          users: usersRes.data?.users || [],
          bills: billsRes.data?.bills || [],
          payments: paymentsRes.data?.payments || [],
          utilities: utilitiesRes.data?.utilities || [],
        });
      } catch (err) {
        console.error('Admin API Error:', err.response || err);
        setError('Failed to fetch admin data. Check credentials or server logs.');
        // If credentials fail during fetch, also redirect
        if (err.response && err.response.status === 401) {
             navigate('/login');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [navigate]);

  // ... (renderHeaders, renderRows, and renderTable functions remain the same) ...
  const renderHeaders = (dataList) => {
    if (dataList.length === 0) return null;
    return (
      <tr>
        {Object.keys(dataList[0]).map((key) => (
          <th key={key}>{key.replace(/_/g, ' ').toUpperCase()}</th>
        ))}
      </tr>
    );
  };

  const renderRows = (dataList) => {
    return dataList.map((item, index) => (
      <tr key={index}>
        {Object.values(item).map((value, i) => (
          <td key={i}>{typeof value === 'object' && value !== null ? JSON.stringify(value) : value}</td>
        ))}
      </tr>
    ));
  };
  
  const renderTable = (dataList) => {
    if (dataList.length === 0) {
      return <p className="no-data">No data found for this section.</p>;
    }
    return (
      <div className="table-responsive">
        <table>
          <thead>
            {renderHeaders(dataList)}
          </thead>
          <tbody>
            {renderRows(dataList)}
          </tbody>
        </table>
      </div>
    );
  };
  
  const TABS = {
    users: { title: 'All Users', data: data.users },
    bills: { title: 'All Bills', data: data.bills },
    payments: { title: 'All Payments', data: data.payments },
    utilities: { title: 'Utilities', data: data.utilities },
  };


  if (loading) {
    return <div className="admin-container">Loading Admin Dashboard...</div>;
  }

  if (error) {
    return <div className="admin-container error-message">{error}</div>;
  }

  return (
    <div className="admin-container">
      <header className="admin-header-flex"> {/* Changed class for better layout */}
        <div className="admin-title-group">
            <h1>Admin Dashboard</h1>
            <p>Overview of all application data.</p>
        </div>
        
        {/* --- NEW LOGOUT BUTTON --- */}
        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
        {/* ------------------------- */}
      </header>
      
      <div className="tab-navigation">
        {Object.keys(TABS).map((key) => (
          <button
            key={key}
            className={`tab-btn ${activeTab === key ? 'active' : ''}`}
            onClick={() => setActiveTab(key)}
          >
            {TABS[key].title} ({TABS[key].data.length})
          </button>
        ))}
      </div>

      <div className="tab-content">
        <h2>{TABS[activeTab].title}</h2>
        {renderTable(TABS[activeTab].data)}
      </div>
    </div>
  );
}

export default AdminPage;