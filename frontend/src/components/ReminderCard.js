import React from 'react';

function ReminderCard({ reminder }) {
  return (
    <div>
      <p>{reminder.message}</p>
      <p>Due by: {reminder.reminder_date}</p>
    </div>
  );
}

export default ReminderCard;
