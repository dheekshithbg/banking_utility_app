# Banking Utility Payment System

A full-stack web application for managing utility bill payments, built with Flask (Python) backend and React frontend.

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Default Credentials](#default-credentials)
- [Features](#features)

---

## Overview

This application allows users to:
- Register and authenticate
- View and manage utility bills (electricity, water, gas)
- Make payments for pending bills
- Set reminders for upcoming due dates
- Admin dashboard for managing users, utilities, bills, and payments

---

## Tech Stack

### Backend
- **Framework**: Flask 3.0.0
- **API**: Flask-RESTful
- **Database**: SQLite3
- **Authentication**: Basic credential-based (JWT placeholder)
- **Password Hashing**: bcrypt
- **CORS**: Flask-CORS

### Frontend
- **Framework**: React 19.2.1
- **Routing**: React Router DOM 7.10.1
- **HTTP Client**: Axios 1.13.2
- **Build Tool**: Create React App (react-scripts 5.0.1)

---

## Project Structure

```
banking_utility_app-main/
├── backend/
│   ├── resources/
│   │   ├── controller.py      # API resource handlers
│   │   └── database.py        # Database operations & models
│   ├── application.py         # Flask app entry point
│   ├── utility_payment_system.db  # SQLite database file
│   └── LICENSE
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── ...
│   ├── src/
│   │   ├── components/
│   │   │   ├── LoginPage.js
│   │   │   ├── RegisterPage.js
│   │   │   ├── HomePage.js
│   │   │   ├── Admin.js
│   │   │   ├── AddServicePage.js
│   │   │   ├── BillCard.js
│   │   │   ├── ReminderCard.js
│   │   │   └── PaymentSuccess.js
│   │   ├── services/
│   │   │   └── api.js         # Axios API configuration
│   │   ├── App.js             # Main React component with routing
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   └── package-lock.json
├── requirements.txt           # Python dependencies
├── Dockerfile
├── package.json
└── README.md
```

---

## Database Schema

### Tables

#### users
| Column | Type | Description |
|--------|------|-------------|
| user_id | INTEGER | Primary key, auto-increment |
| username | TEXT | Unique username |
| password_hash | TEXT | bcrypt hashed password |
| email | TEXT | User email |
| phone_number | TEXT | Phone number |
| pan | TEXT | Unique PAN number (Indian tax ID) |
| aadhaar | TEXT | Unique Aadhaar number (Indian ID) |
| role | TEXT | 'user' or 'admin' |
| created_at | TEXT | Timestamp |

#### utilities
| Column | Type | Description |
|--------|------|-------------|
| utility_id | INTEGER | Primary key |
| name | TEXT | Utility name (Electricity, Water, Gas) |
| description | TEXT | Description |
| provider_name | TEXT | Service provider name |
| created_at | TEXT | Timestamp |

#### bills
| Column | Type | Description |
|--------|------|-------------|
| bill_id | INTEGER | Primary key |
| user_id | INTEGER | Foreign key to users |
| utility_id | INTEGER | Foreign key to utilities |
| amount | REAL | Bill amount |
| due_date | TEXT | Payment due date |
| status | TEXT | 'pending' or 'paid' |
| created_at | TEXT | Timestamp |

#### payments
| Column | Type | Description |
|--------|------|-------------|
| payment_id | INTEGER | Primary key |
| bill_id | INTEGER | Foreign key to bills |
| user_id | INTEGER | Foreign key to users |
| amount | REAL | Payment amount |
| payment_method | TEXT | Payment method used |
| status | TEXT | Payment status |
| transaction_date | TEXT | Transaction timestamp |

#### reminders
| Column | Type | Description |
|--------|------|-------------|
| reminder_id | INTEGER | Primary key |
| user_id | INTEGER | Foreign key to users |
| message | TEXT | Reminder message |
| reminder_date | TEXT | Date for reminder |
| created_at | TEXT | Timestamp |

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/register` | User registration |
| POST | `/api/auth/logout` | User logout |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/<userId>` | Get user details |
| PUT | `/api/users/<userId>` | Update user profile |

### Utilities
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/utilities` | List all utilities |
| POST | `/api/utilities` | Add new utility (Admin) |
| GET | `/api/utilities/<utilityId>` | Get utility details |
| PUT | `/api/utilities/<utilityId>` | Update utility (Admin) |
| DELETE | `/api/utilities/<utilityId>` | Delete utility (Admin) |
| GET | `/api/utilities/user/<user_id>` | Get utilities for a user |

### Bills
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bills/<user_id>` | Get bills for user |
| POST | `/api/bills` | Create new bill |
| GET | `/api/bills/<billId>` | Get bill details |
| PUT | `/api/bills/<billId>` | Update bill |
| DELETE | `/api/bills/<billId>` | Delete bill |

### Payments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/payments/<user_id>` | Get payments for user |
| POST | `/api/payments/<user_id>` | Make a payment |
| GET | `/api/payments/<paymentId>` | Get payment details |
| PUT | `/api/payments/<paymentId>` | Update payment status |
| DELETE | `/api/payments/<paymentId>` | Delete payment |

### Reminders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reminders/<user_id>` | Get reminders for user |
| POST | `/api/reminders/<user_id>` | Create reminder |
| DELETE | `/api/reminders/<reminderId>` | Delete reminder |

### Admin Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/users` | List all users |
| GET | `/api/admin/utilities` | List all utilities |
| GET | `/api/admin/bills` | List all bills |
| GET | `/api/admin/payments` | List all payments |

**Admin Authentication**: Admin endpoints require `X-USERNAME` and `X-PASSWORD` headers.

---

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+ and npm
- pip (Python package manager)

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd banking_utility_app-main/backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install flask flask-restful flask-cors bcrypt
   ```
   
   Or install all dependencies from requirements.txt (from project root):
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Run the backend server:**
   ```bash
   python application.py
   ```
   
   The backend will:
   - Create the SQLite database tables automatically
   - Insert dummy data for testing
   - Start the Flask server on `http://localhost:5000`

   You should see:
   ```
   Tables created successfully.
   Inserting dummy data...
   Dummy data insertion complete.
   * Running on http://127.0.0.1:5000
   ```

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd banking_utility_app-main/frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Configure the API URL:**
   
   Edit `src/services/api.js` and update the `baseURL` to match your backend:
   ```javascript
   const API = axios.create({
     baseURL: 'http://localhost:5000/api',
   });
   ```

4. **Start the React development server:**
   ```bash
   npm start
   ```
   
   The frontend will start on `http://localhost:3000`

---

## Default Credentials

### Test Users (created by dummy data)

| Username | Password | Role |
|----------|----------|------|
| john_doe | password123 | user |
| alice_smith | adminpass | admin |
| bob_jones | password123 | user |
| carol_white | password123 | user |
| david_black | password123 | user |

### Admin API Access
- Username: `admin`
- Password: `admin123`

Pass these as headers:
```
X-USERNAME: admin
X-PASSWORD: admin123
```

---

## Features

### User Features
- **Authentication**: Register with PAN/Aadhaar validation, login/logout
- **Dashboard**: View pending bills and payment history
- **Bill Payment**: Pay utility bills with various payment methods
- **Reminders**: Set and manage payment reminders
- **Profile Management**: Update email and phone number

### Admin Features
- **User Management**: View all registered users
- **Utility Management**: Add, edit, delete utility providers
- **Bill Management**: Create and manage bills for users
- **Payment Tracking**: View all payment transactions

### Frontend Routes
| Path | Component | Description |
|------|-----------|-------------|
| `/` | LoginPage | Default landing/login page |
| `/login` | LoginPage | User login |
| `/register` | RegisterPage | New user registration |
| `/home` | HomePage | User dashboard |
| `/admin` | AdminPage | Admin dashboard |
| `/add_service` | AddServicePage | Add new utility service |
| `/payment-success` | PaymentSuccess | Payment confirmation |

---

## License

This project is licensed under the terms included in the LICENSE file.
