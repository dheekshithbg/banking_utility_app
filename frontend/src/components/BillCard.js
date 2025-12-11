import React from 'react';

function BillCard({ utility, bills }) {
  const utilityBills = bills.filter((bill) => bill.utility_id === utility.utility_id);

  return (
    <div>
      <h4>{utility.name}</h4>
      <p>{utility.description}</p>
      <p>Provider: {utility.provider_name}</p>
      <ul>
        {utilityBills.map((bill) => (
          <li key={bill.bill_id}>
            <p>Amount: ₹{bill.amount}</p>
            <p>Due Date: {bill.due_date}</p>
            <button>Make Payment</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default BillCard;
