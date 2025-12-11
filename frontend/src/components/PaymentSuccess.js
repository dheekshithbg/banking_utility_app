import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

function PaymentSuccess() {
  const navigate = useNavigate();
  const location = useLocation();
  
  // Get payment details from navigation state (if provided)
  const paymentData = location.state || {
    amount: 'N/A',
    date: new Date().toLocaleDateString(),
    transactionId: 'TXN' + Math.random().toString(9).substr(2, 9).toUpperCase(),
  };

  const handlePrintReceipt = () => {
    // Trigger browser print dialog
    window.print();
  };

  const handleBackToHome = () => {
    navigate('/home');
  };

  return (
    <div className="payment-success-wrapper">
      {/* Full-screen Background */}
      <div className="payment-success-background"></div>

      {/* Success Card */}
      <div className="payment-success-card">
        {/* Success Icon */}
        <div className="success-icon">
          <svg
            width="100"
            height="100"
            viewBox="0 0 100 100"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle cx="50" cy="50" r="48" stroke="#4CAF50" strokeWidth="2" />
            <path
              d="M30 50L45 65L70 35"
              stroke="#4CAF50"
              strokeWidth="4"
              strokeLinecap="round"
              strokeLinejoin="round"
              fill="none"
            />
          </svg>
        </div>

        {/* Success Message */}
        <h1 className="success-title">Payment Successful! 🎉</h1>
        <p className="success-subtitle">
          Your payment has been processed successfully and stored in the database.
        </p>

        {/* Receipt Details */}
        <div className="receipt-details">
          <div className="receipt-row">
            <span className="label">Amount Paid:</span>
            <span className="value">Rs. {paymentData.amount}</span>
          </div>
          <div className="receipt-row">
            <span className="label">Date & Time:</span>
            <span className="value">{paymentData.date}</span>
          </div>
          <div className="receipt-row">
            <span className="label">Transaction ID:</span>
            <span className="value">{paymentData.transactionId}</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="action-buttons">
          <button onClick={handlePrintReceipt} className="print-btn">
            🖨️ Print Receipt
          </button>
          <button onClick={handleBackToHome} className="back-home-btn">
            Back to Home
          </button>
        </div>

        {/* Print Styles - Hidden from display but used by print dialog */}
        <style>{`
          @media print {
            .payment-success-wrapper {
              background: white !important;
            }
            .payment-success-background {
              display: none;
            }
            .payment-success-card {
              box-shadow: none !important;
              border: 1px solid #ddd !important;
              background: white !important;
            }
            .action-buttons {
              display: none;
            }
            .success-icon {
              page-break-after: avoid;
            }
          }
        `}</style>
      </div>
    </div>
  );
}

export default PaymentSuccess;
