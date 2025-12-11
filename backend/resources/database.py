import sqlite3
from sqlite3 import Error
import bcrypt
import re
from datetime import datetime

DATABASE = "utility_payment_system.db"

# --- Connection and Setup ---

def create_connection():
    """Create and return a database connection."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        conn.row_factory = sqlite3.Row
    except Error as e:
        print(f"Error while connecting to SQLite: {e}")
    return conn

def create_table():
    """Create tables in the database."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            cursor.execute("DROP TABLE IF EXISTS payments;")
            cursor.execute("DROP TABLE IF EXISTS reminders;")
            cursor.execute("DROP TABLE IF EXISTS bills;")
            cursor.execute("DROP TABLE IF EXISTS utilities;")
            cursor.execute("DROP TABLE IF EXISTS users;")
            
            # Create users table
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL UNIQUE,
                                password_hash TEXT NOT NULL,
                                email TEXT NOT NULL,
                                phone_number TEXT NOT NULL,
                                pan TEXT UNIQUE,
                                aadhaar TEXT UNIQUE,
                                role TEXT NOT NULL DEFAULT 'user',
                                created_at TEXT NOT NULL);''')

            # Create utilities table
            cursor.execute('''CREATE TABLE IF NOT EXISTS utilities (
                                utility_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                description TEXT,
                                provider_name TEXT,
                                created_at TEXT NOT NULL);''')

            # Create bills table
            cursor.execute('''CREATE TABLE IF NOT EXISTS bills (
                                bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER NOT NULL,
                                utility_id INTEGER NOT NULL,
                                amount REAL NOT NULL,
                                due_date TEXT NOT NULL,
                                status TEXT NOT NULL DEFAULT 'pending',
                                created_at TEXT NOT NULL, 
                                FOREIGN KEY (user_id) REFERENCES users (user_id),
                                FOREIGN KEY (utility_id) REFERENCES utilities (utility_id));''')

            # Create payments table
            cursor.execute('''CREATE TABLE IF NOT EXISTS payments (
                                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                bill_id INTEGER NOT NULL,
                                user_id INTEGER NOT NULL,
                                amount REAL NOT NULL,
                                payment_method TEXT NOT NULL,
                                status TEXT NOT NULL DEFAULT 'completed',
                                transaction_date TEXT NOT NULL,
                                FOREIGN KEY (bill_id) REFERENCES bills (bill_id),
                                FOREIGN KEY (user_id) REFERENCES users (user_id));''')

            # Create reminders table
            cursor.execute('''CREATE TABLE IF NOT EXISTS reminders (
                                reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER NOT NULL,
                                message TEXT NOT NULL,
                                reminder_date TEXT NOT NULL,
                                created_at TEXT NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES users (user_id));''')

            conn.commit()
            print("Tables created successfully.")
        except Error as e:
            print(f"Error while creating tables: {e}")
        finally:
            conn.close()

# --- Validation Functions ---

def is_valid_pan(pan):
    """Validate PAN number using a simple regex (example format: ABCDE1234F)."""
    pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    return re.match(pan_pattern, pan) is not None

def is_valid_aadhaar(aadhaar):
    """Validate Aadhaar number using a simple regex (12 digits)."""
    aadhaar_pattern = r'^\d{12}$'
    return re.match(aadhaar_pattern, aadhaar) is not None

# --- User Management Functions ---

def add_user(username, password, email, phone_number, pan=None, aadhaar=None, role='user'):
    """Add a new user to the users table."""
    if pan and not is_valid_pan(pan):
        return "Invalid PAN format."
    if aadhaar and not is_valid_aadhaar(aadhaar):
        return "Invalid Aadhaar format."

    conn = create_connection()
    if conn:
        try:
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO users (username, password_hash, email, phone_number, pan, aadhaar, role, created_at)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                           (username, password_hash, email, phone_number, pan, aadhaar, role, created_at))
            conn.commit()
            return True
        except Error as e:
            return str(e)
        finally:
            if conn: conn.close()
            
def get_all_users():
    """Retrieve all users (Admin)."""
    conn = create_connection()
    users = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
        except Error as e:
            print(f"Error while fetching users: {e}")
        finally:
            conn.close()
    return users
            
def get_user_by_id(user_id):
    """Retrieve a user by their user_id."""
    conn = create_connection()
    user = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM users WHERE user_id = ?;''', (user_id,))
            user = cursor.fetchone()
        except Error as e:
            print(f"Error while fetching user: {e}")
        finally:
            conn.close()
    return user
    
def get_user_by_username(username):
    """Retrieve a user by their username."""
    conn = create_connection()
    user = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM users WHERE username = ?;''', (username,))
            user = cursor.fetchone()
        except Error as e:
            print(f"Error while fetching user: {e}")
        finally:
            conn.close()
    return user

def check_password(user, password):
    """Check if the provided password matches the stored password."""
    if not user:
        return False
    stored_hash = user['password_hash'].encode('utf-8') if isinstance(user['password_hash'], str) else user['password_hash']
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

# --- Utility Management Functions (CRUD) ---
def add_utility(name, description, provider_name):
    """Add a utility to the utilities table."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO utilities (name, description, provider_name, created_at)
                             VALUES (?, ?, ?, ?)''', 
                           (name, description, provider_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            return None
        finally:
            if conn: conn.close()

def get_all_utilities():
    """Retrieve all utilities."""
    conn = create_connection()
    utilities = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM utilities;")
            utilities = cursor.fetchall()
        except Error as e:
            print(f"Error while fetching utilities: {e}")
        finally:
            conn.close()
    return utilities

def get_utility_by_id(utility_id):
    """Retrieve a utility by its ID."""
    conn = create_connection()
    utility = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM utilities WHERE utility_id = ?;''', (utility_id,))
            utility = cursor.fetchone()
        except Error as e:
            print(f"Error while fetching utility: {e}")
        finally:
            conn.close()
    return utility
def get_utilities_by_user(user_id):
    """Retrieve a utility by its ID."""
    conn = create_connection()
    utility = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM bills WHERE user_id = ?;''', (user_id,))
            utility = cursor.fetchall()
        except Error as e:
            print(f"Error while fetching utility: {e}")
        finally:
            conn.close()
    return utility

def update_utility(utility_id, name=None, description=None, provider_name=None):
    """Update utility details."""
    conn = create_connection()
    if conn:
        try:
            updates = []
            params = []
            
            if name:
                updates.append("name = ?")
                params.append(name)
            if description:
                updates.append("description = ?")
                params.append(description)
            if provider_name:
                updates.append("provider_name = ?")
                params.append(provider_name)
                
            if not updates:
                return "No fields to update."
            
            sql = f"UPDATE utilities SET {', '.join(updates)} WHERE utility_id = ?"
            params.append(utility_id)
            
            cursor = conn.cursor()
            cursor.execute(sql, tuple(params))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            return str(e)
        finally:
            if conn: conn.close()
            
def delete_utility(utility_id):
    """Delete a utility."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM utilities WHERE utility_id = ?;", (utility_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            return str(e)
        finally:
            if conn: conn.close()

# --- Bill Management Functions (CRUD) ---
def add_bill(user_id, utility_id, amount, due_date):
    """Add a bill for a user."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO bills (user_id, utility_id, amount, due_date, status, created_at)
                             VALUES (?, ?, ?, ?, ?, ?)''', 
                           (user_id, utility_id, amount, due_date, 'pending', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            return None
        finally:
            if conn: conn.close()
            
def get_all_bills():
    """Retrieve all bills, joining with user and utility names."""
    conn = create_connection()
    bills = []
    if conn:
        try:
            cursor = conn.cursor()
            sql = '''
            SELECT 
                b.*, 
                u.username AS username, 
                util.name AS utility_name,
                util.provider_name AS provider_name
            FROM bills b
            JOIN users u ON b.user_id = u.user_id
            JOIN utilities util ON b.utility_id = util.utility_id
            ORDER BY b.due_date DESC;
            '''
            cursor.execute(sql)
            bills = cursor.fetchall()
        except Error as e:
            print(f"Error fetching all bills: {e}")
        finally:
            conn.close()
    return bills

def get_all_payments():
    """Retrieve all payments, joining with user and bill details."""
    conn = create_connection()
    payments = []
    if conn:
        try:
            cursor = conn.cursor()
            sql = '''
            SELECT 
                p.*, 
                u.username AS username, 
                b.amount AS bill_amount,
                util.name AS utility_name
            FROM payments p
            JOIN users u ON p.user_id = u.user_id
            JOIN bills b ON p.bill_id = b.bill_id
            JOIN utilities util ON b.utility_id = util.utility_id
            ORDER BY p.payment_date DESC;
            '''
            cursor.execute(sql)
            payments = cursor.fetchall()
        except Error as e:
            print(f"Error fetching all payments: {e}")
        finally:
            conn.close()
    return payments

def get_bill_by_id(bill_id):
    """Retrieve a bill by its ID."""
    conn = create_connection()
    bill = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM bills WHERE bill_id = ?;''', (bill_id,))
            bill = cursor.fetchone()
        except Error as e:
            print(f"Error while fetching bill: {e}")
        finally:
            conn.close()
    return bill

def get_bills_by_user(user_id, status=None):
    """Retrieve all bills for a specific user, including utility name and provider."""
    conn = create_connection()
    bills = []
    if conn:
        try:
            cursor = conn.cursor()
            
            # **UPDATED SQL QUERY with JOIN:**
            # Joins 'bills' (b) with 'utilities' (u) to get utility details.
            sql = '''SELECT 
                         b.*, 
                         u.name AS utility_name, 
                         u.provider_name AS provider_name
                     FROM bills b
                     JOIN utilities u ON b.utility_id = u.utility_id
                     WHERE b.user_id = ?
            '''
            params = [user_id]
            
            if status:
                sql += " AND b.status = ?"
                params.append(status)
                
            sql += " ORDER BY b.due_date ASC;"

            cursor.execute(sql, tuple(params))
            bills = cursor.fetchall()
            
        except Error as e:
            print(f"Error while fetching bills for user {user_id}: {e}")
        finally:
            conn.close()
    return bills

def update_bill(bill_id, amount=None, due_date=None, status=None):
    """Update bill details."""
    conn = create_connection()
    if conn:
        try:
            updates = []
            params = []
            
            if amount is not None:
                updates.append("amount = ?")
                params.append(amount)
            if due_date:
                updates.append("due_date = ?")
                params.append(due_date)
            if status:
                updates.append("status = ?")
                params.append(status)
                
            if not updates:
                return "No fields to update."
            
            sql = f"UPDATE bills SET {', '.join(updates)} WHERE bill_id = ?"
            params.append(bill_id)
            
            cursor = conn.cursor()
            cursor.execute(sql, tuple(params))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            return str(e)
        finally:
            if conn: conn.close()
            
def delete_bill(bill_id):
    """Delete a bill."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bills WHERE bill_id = ?;", (bill_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            return str(e)
        finally:
            if conn: conn.close()

# --- Payment Management Functions (CRUD) ---
def add_payment(bill_id, user_id, amount, payment_method, status='completed'):
    """Record a new payment for a bill."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO payments (bill_id, user_id, amount, payment_method, status, transaction_date)
                             VALUES (?, ?, ?, ?, ?, ?)''', 
                           (bill_id, user_id, amount, payment_method, status, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            payment_id = cursor.lastrowid
            
            if status == 'completed':
                update_bill(bill_id, status='paid')
                
            conn.commit()
            return payment_id
        except Error as e:
            return None
        finally:
            if conn: conn.close()
            
def get_payment_by_id(payment_id):
    """Retrieve a payment by its ID."""
    conn = create_connection()
    payment = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM payments WHERE payment_id = ?;''', (payment_id,))
            payment = cursor.fetchone()
        except Error as e:
            print(f"Error while fetching payment: {e}")
        finally:
            conn.close()
    return payment

def get_payments_by_bill(bill_id):
    """Retrieve all payments for a specific bill."""
    conn = create_connection()
    payments = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM payments WHERE bill_id = ? ORDER BY transaction_date DESC;", (bill_id,))
            payments = cursor.fetchall()
        except Error as e:
            print(f"Error while fetching payments for bill {bill_id}: {e}")
        finally:
            conn.close()
    return payments

def get_payments_by_user(user_id):
    """Retrieve all payments made by a specific user."""
    conn = create_connection()
    payments = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM payments WHERE user_id = ? ORDER BY transaction_date DESC;", (user_id,))
            payments = cursor.fetchall()
        except Error as e:
            print(f"Error while fetching payments for user {user_id}: {e}")
        finally:
            conn.close()
    return payments

# --- Reminders Management Functions (CRUD) ---
def add_reminder(user_id, message, reminder_date):
    """Add a reminder for the user."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO reminders (user_id, message, reminder_date, created_at)
                             VALUES (?, ?, ?, ?)''', 
                           (user_id, message, reminder_date, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            return None
        finally:
            if conn: conn.close()

def get_reminders_by_user(user_id):
    """Retrieve all reminders for a specific user."""
    conn = create_connection()
    reminders = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reminders WHERE user_id = ? ORDER BY reminder_date ASC;", (user_id,))
            reminders = cursor.fetchall()
        except Error as e:
            print(f"Error while fetching reminders for user {user_id}: {e}")
        finally:
            conn.close()
    return reminders

def delete_reminder(reminder_id):
    """Delete a reminder."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reminders WHERE reminder_id = ?;", (reminder_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            return str(e)
        finally:
            if conn: conn.close()

# --- Initial Data & Execution Block ---

def insert_dummy_data():
    
    """Insert dummy data into the tables."""
    print("Inserting dummy data...")
    add_user("john_doe", "password123", "john@example.com", "9876543210", pan="ABCDE1234F", aadhaar="123456789012", role="user")
    add_user("alice_smith", "adminpass", "alice@example.com", "9876543211", pan="ABCDE5678G", aadhaar="123456789013", role="admin")
    add_user("bob_jones", "password123", "bob@example.com", "9876543212", pan="ABCDE9012H", aadhaar="123456789014", role="user")
    add_user("carol_white", "password123", "carol@example.com", "9876543213", pan="ABCDE3456J", aadhaar="123456789015", role="user")
    add_user("david_black", "password123", "david@example.com", "9876543214", pan="ABCDE7890K", aadhaar="123456789016", role="user")
    
    add_utility("Electricity", "Electricity supply for the city", "XYZ Power Co.")
    add_utility("Water", "Water supply for households", "ABC Water Works")
    add_utility("Water", "Water supply for households", "DEF Water Solutions")
    add_utility("Gas", "Natural gas supply for homes", "DEF Gas Ltd.")
    
    add_bill(1, 1, 120.50, "2025-12-15") 
    add_bill(2, 2, 75.00, "2025-12-10")
    add_bill(2,1,100.00,"2026-01-01")
    add_bill(3, 3, 60.00, "2025-12-20")
    add_bill(4, 1, 50.00, "2025-12-18")
    add_bill(5, 2, 90.00, "2025-12-16")
    
    add_payment(bill_id=1, user_id=1, amount=120.50, payment_method="credit_card")
    
    add_reminder(1, "Pay electricity bill by 2025-12-15", "2025-12-14")
    add_reminder(2, "Pay water bill by 2025-12-10", "2025-12-09")
    add_reminder(3, "Pay gas bill by 2025-12-20", "2025-12-19")
    
    print("Dummy data insertion complete.")
    
def fetch_all_data():
    """Fetch all users, utilities, bills, reminders, and payments."""
    conn = create_connection()
    users, utilities, bills, reminders, payments = [], [], [], [], []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
            cursor.execute("SELECT * FROM utilities;")
            utilities = cursor.fetchall()
            cursor.execute("SELECT * FROM bills;")
            bills = cursor.fetchall()
            cursor.execute("SELECT * FROM reminders;")
            reminders = cursor.fetchall()
            cursor.execute("SELECT * FROM payments;")
            payments = cursor.fetchall()
            
            users = [dict(row) for row in users]
            utilities = [dict(row) for row in utilities]
            bills = [dict(row) for row in bills]
            reminders = [dict(row) for row in reminders]
            payments = [dict(row) for row in payments]
            return users, utilities, bills, reminders, payments
        except Error as e:
            print(f"Error while fetching data: {e}")
        finally:
            conn.close()
    return users, utilities, bills, reminders, payments

if __name__ == "__main__":
    create_table()
    
    insert_dummy_data()

    users, utilities, bills, reminders, payments = fetch_all_data()

    print("\n--- Verification of Initial Data ---")
    print("\nUsers:")
    for user in users:
        user_info = dict(user)
        user_info['password_hash'] = '***HASHED***'
        print(user_info)

    print("\nBills:")
    for bill in bills:
        print(bill)

    print("\nPayments:")
    for payment in payments:
        print(payment)
    print("------------------------------------")