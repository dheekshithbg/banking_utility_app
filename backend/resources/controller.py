from flask import request
from flask_restful import Resource
from resources import database as db
from flask_cors import cross_origin
# ================================

# BASIC SECURITY (Username + Password)

# ================================

VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"

def check_credentials():
    username = request.headers.get("X-USERNAME")
    password = request.headers.get("X-PASSWORD")
    if username != VALID_USERNAME or password != VALID_PASSWORD:
        return False
    return True

# Helper function to convert sqlite3.Row to a standard dictionary
def row_to_dict(row):
    if row is None:
        return None
    # Assuming the database connection sets row_factory to sqlite3.Row
    return dict(row)

# ==============================================================================
# 🌟 Authentication Endpoints 🌟
# ==============================================================================

class LoginResource(Resource):
    def post(self):
        """POST /api/auth/login"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return {'message': 'Username and password are required'}, 400

        user = db.get_user_by_username(username)

        if user and db.check_password(user, password):
            # In a real app, a JWT token would be generated here
            return {'message': 'Login successful', 'token': 'dummy_jwt_token_for_user' , 'user_id': user['user_id']}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

class RegisterResource(Resource):
    def post(self):
        """POST /api/auth/register"""
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')
        pan = data.get('pan')
        aadhaar = data.get('aadhaar')
        
        if not all([username, email, phone_number, password]):
            return {'message': 'Missing required fields: username, email, phone_number, password'}, 400

        result = db.add_user(username, password, email, phone_number, pan, aadhaar, role='user')
        
        if result is True:
            return {'message': f'User {username} registered successfully.'}, 201
        elif isinstance(result, str) and "UNIQUE constraint failed" in result:
            return {'message': 'Registration failed: Username, PAN, or Aadhaar already exists.'}, 409
        elif isinstance(result, str):
            return {'message': f'Registration failed: {result}'}, 400
        else:
            return {'message': 'Registration failed due to unknown error.'}, 500

class LogoutResource(Resource):
    def post(self):
        """POST /api/auth/logout - Stub for JWT invalidation"""
        # In a real app, this would blacklist the token or clear a session/cookie.
        return {'message': 'Logout successful. (JWT Token invalidated)'}, 200

# ==============================================================================
# 👤 User Management Endpoints 👤
# ==============================================================================

class UserDetailResource(Resource):
    def get(self, userId):
        """GET /api/users/{userId}"""
        # Auth check (should ensure the requester is the user OR an admin)
        
        user = db.get_user_by_id(userId)
        if not user:
            return {'message': 'User not found'}, 404
        
        user_dict = row_to_dict(user)
        # Never expose the password hash
        del user_dict['password_hash']
        
        return {'user': user_dict}, 200

    def put(self, userId):
        """PUT /api/users/{userId}"""
        # Auth check (should ensure the requester is the user OR an admin)
        
        data = request.get_json()
        email = data.get('email')
        phone_number = data.get('phone_number')
        
        if not email and not phone_number:
            return {'message': 'Provide email or phone_number to update'}, 400
        
        result = db.update_user(userId, email=email, phone_number=phone_number)
        
        if result is True:
            updated_user = db.get_user_by_id(userId)
            if updated_user:
                updated_user_dict = row_to_dict(updated_user)
                del updated_user_dict['password_hash']
                return {'message': 'User updated successfully', 'user': updated_user_dict}, 200
            return {'message': 'User updated, but failed to fetch details'}, 200
        elif isinstance(result, str):
            return {'message': f'Update failed: {result}'}, 500
        else:
            return {'message': 'User not found or no change made'}, 404

# ==============================================================================
# 💡 Utility Management Endpoints 💡
# ==============================================================================

class UtilityListResource(Resource):
    def get(self):
        """GET /api/utilities"""
        utilities = db.get_all_utilities()
        return {'utilities': [row_to_dict(u) for u in utilities]}, 200

    def post(self):
        """POST /api/utilities"""
        # Admin Auth check required
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        provider_name = data.get('provider_name')
        
        if not all([name, description, provider_name]):
            return {'message': 'Missing required fields: name, description, provider_name'}, 400

        utility_id = db.add_utility(name, description, provider_name)
        
        if utility_id:
            return {'message': 'Utility added successfully', 'utility_id': utility_id}, 201
        else:
            return {'message': 'Failed to add utility'}, 500

class UtilityDetailResource(Resource):
    def get(self, utilityId):
        """GET /api/utilities/{utilityId}"""
        utility = db.get_utility_by_id(utilityId)
        if not utility:
            return {'message': 'Utility not found'}, 404
        return {'utility': row_to_dict(utility)}, 200

    def put(self, utilityId):
        """PUT /api/utilities/{utilityId}"""
        # Admin Auth check required
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        provider_name = data.get('provider_name')
        
        result = db.update_utility(utilityId, name, description, provider_name)
        
        if result is True:
            return {'message': 'Utility updated successfully'}, 200
        elif isinstance(result, str):
            return {'message': f'Update failed: {result}'}, 500
        else:
            return {'message': 'Utility not found or no change made'}, 404

    def delete(self, utilityId):
        """DELETE /api/utilities/{utilityId}"""
        # Admin Auth check required
        result = db.delete_utility(utilityId)
        
        if result is True:
            return {'message': 'Utility deleted successfully'}, 200
        elif isinstance(result, str):
            return {'message': f'Deletion failed: {result}'}, 500
        else:
            return {'message': 'Utility not found'}, 404

# ==============================================================================
# 💰 Bill Management Endpoints 💰
# ==============================================================================

class BillListResource(Resource):
    def get(self, current_user_id):
        """GET /api/bills - Get bills for the authenticated user"""
        # Placeholder for current user ID (should be retrieved from JWT)
        # Using a dummy ID for demonstration without Auth
        # In a real app: current_user_id = decode_jwt().get('user_id')
        # current_user_id = 1 
        
        bills = db.get_bills_by_user(current_user_id)
        return {'bills': [row_to_dict(b) for b in bills]}, 200

class UserUtilityListResource(Resource):
    
    # ⚠️ Use the cross_origin decorator to ensure CORS headers are added.
    @cross_origin() 
    def get(self, user_id):
        """GET /api/utilities/user/<int:user_id> - Get utilities associated with a user."""
        
        # 1. (Optional) Security Check: Ensure the requested user_id matches the authenticated token's user_id
        # if user_id != token_user_id: 
        #     return {'message': 'Unauthorized access to user utilities'}, 403 
        
        try:
            # Assume db.get_utilities_by_user returns a list of utility objects/rows
            utilities = db.get_utilities_by_user(user_id)
            
            # Ensure your db function is implemented to handle this query:
            # SELECT * FROM utilities WHERE user_id = ? (or linked via a mapping table)
            
            return {'utilities': [row_to_dict(u) for u in utilities]}, 200
        
        except Exception as e:
            print(f"Error fetching user utilities for ID {user_id}: {e}")
            return {'message': 'Internal Server Error while fetching utilities.'}, 500
class AddBillResource(Resource):
    def post(self):
        """POST /api/bills - Generate a new bill (Admin/System only)"""
        # Admin/System Auth check required
        data = request.get_json()
        user_id = data.get('user_id')
        utility_id = data.get('utility_id')
        amount = data.get('amount')
        due_date = data.get('due_date') # NOTE: Bill date/created_at is handled by DB function
        
        if not all([user_id, utility_id, amount, due_date]):
            return {'message': 'Missing required fields: user_id, utility_id, amount, due_date'}, 400

        bill_id = db.add_bill(user_id, utility_id, amount, due_date)
        
        if bill_id:
            return {'message': 'Bill created successfully', 'bill_id': bill_id}, 201
        else:
            return {'message': 'Failed to create bill. Check user/utility IDs.'}, 500

class BillDetailResource(Resource):
    def get(self, billId):
        """GET /api/bills/{billId}"""
        # Auth check (should ensure the requester is the bill's user OR an admin)
        
        bill = db.get_bill_by_id(billId)
        if not bill:
            return {'message': 'Bill not found'}, 404
            
        # Add bill user ownership check here
            
        return {'bill': row_to_dict(bill)}, 200

    def put(self, billId):
        """PUT /api/bills/{billId}"""
        # Admin Auth check or special permission required (e.g., status update only)
        data = request.get_json()
        amount = data.get('amount')
        due_date = data.get('due_date')
        status = data.get('status')
        
        result = db.update_bill(billId, amount=amount, due_date=due_date, status=status)
        
        if result is True:
            return {'message': 'Bill updated successfully'}, 200
        elif isinstance(result, str):
            return {'message': f'Update failed: {result}'}, 500
        else:
            return {'message': 'Bill not found or no change made'}, 404

    def delete(self, billId):
        """DELETE /api/bills/{billId}"""
        # Admin Auth check required
        result = db.delete_bill(billId)
        
        if result is True:
            return {'message': 'Bill deleted successfully'}, 200
        elif isinstance(result, str):
            return {'message': f'Deletion failed: {result}'}, 500
        else:
            return {'message': 'Bill not found'}, 404

# ==============================================================================
# 💳 Payment Management Endpoints 💳
# ==============================================================================

class PaymentListResource(Resource):
    def get(self, current_user_id):
        """GET /api/payments - Get payments for the authenticated user"""
        # Placeholder for current user ID (should be retrieved from JWT)
        # In a real app: current_user_id = decode_jwt().get('user_id')
        # current_user_id = 1 
        
        payments = db.get_payments_by_user(current_user_id)
        return {'payments': [row_to_dict(p) for p in payments]}, 200

    def post(self):
        """POST /api/payments - Make a payment for a bill."""
        data = request.get_json()
        bill_id = data.get('bill_id')
        user_id = data.get('user_id')
        payment_amount = data.get('payment_amount')
        payment_method = data.get('payment_method')
        
        if not all([bill_id, user_id, payment_amount, payment_method]):
            return {'message': 'Missing required fields: bill_id, user_id, payment_amount, payment_method'}, 400
        
        # In a real app, this would involve a call to an external payment gateway.
        # For simulation, we assume immediate completion.
        payment_id = db.add_payment(bill_id, user_id, payment_amount, payment_method, status='completed')

        if payment_id:
            return {'message': 'Payment successful', 'payment_id': payment_id}, 201
        else:
            return {'message': 'Payment processing failed'}, 500

class PaymentDetailResource(Resource):
    def get(self, paymentId):
        """GET /api/payments/{paymentId}"""
        # Auth check (should ensure the requester is the payment's user OR an admin)
        
        payment = db.get_payment_by_id(paymentId)
        if not payment:
            return {'message': 'Payment not found'}, 404
        
        # Add payment user ownership check here
            
        return {'payment': row_to_dict(payment)}, 200

    def put(self, paymentId):
        """PUT /api/payments/{paymentId}"""
        # Admin/System Auth check required (usually only status updates)
        data = request.get_json()
        status = data.get('status')
        
        if not status:
            return {'message': 'Provide status field to update'}, 400
        
        result = db.update_payment(paymentId, status=status)
        
        if result is True:
            return {'message': 'Payment updated successfully'}, 200
        elif isinstance(result, str):
            return {'message': f'Update failed: {result}'}, 500
        else:
            return {'message': 'Payment not found or no change made'}, 404

    def delete(self, paymentId):
        """DELETE /api/payments/{paymentId}"""
        # Admin Auth check required
        result = db.delete_payment(paymentId)
        
        if result is True:
            return {'message': 'Payment deleted successfully'}, 200
        elif isinstance(result, str):
            return {'message': f'Deletion failed: {result}'}, 500
        else:
            return {'message': 'Payment not found'}, 404

# ==============================================================================
# 🔔 Reminders & Notifications Endpoints 🔔
# ==============================================================================

class ReminderListResource(Resource):
    def get(self, current_user_id):
        """GET /api/reminders/current_user_id - Get reminders for the authenticated user"""
        # Placeholder for current user ID (should be retrieved from JWT)
        # In a real app: current_user_id = decode_jwt().get('user_id')
        # current_user_id = 1 
        
        reminders = db.get_reminders_by_user(current_user_id)
        return {'reminders': [row_to_dict(r) for r in reminders]}, 200

    def post(self):
        """POST /api/reminders - Create a new reminder."""
        data = request.get_json()
        user_id = data.get('user_id')
        # bill_id is in the request but not directly stored in the reminder table
        # We will use it to construct a message, or assume it's used by a logic layer
        bill_id = data.get('bill_id') 
        reminder_date = data.get('reminder_date')
        
        if not all([user_id, bill_id, reminder_date]):
            return {'message': 'Missing required fields: user_id, bill_id, reminder_date'}, 400
        
        # Retrieve bill information to create a meaningful message
        bill = db.get_bill_by_id(bill_id)
        if not bill:
            return {'message': 'Bill not found'}, 404
            
        # Simple message for demonstration
        message = f"Reminder to pay Bill ID {bill_id} (Amount: {bill['amount']}) by {bill['due_date']}"

        reminder_id = db.add_reminder(user_id, message, reminder_date)

        if reminder_id:
            return {'message': 'Reminder created successfully', 'reminder_id': reminder_id}, 201
        else:
            return {'message': 'Failed to create reminder'}, 500

class ReminderDetailResource(Resource):
    def delete(self, reminderId):
        """DELETE /api/reminders/{reminderId}"""
        # Auth check (should ensure the requester is the reminder's user OR an admin)
        
        result = db.delete_reminder(reminderId)
        
        if result is True:
            return {'message': 'Reminder deleted successfully'}, 200
        elif isinstance(result, str):
            return {'message': f'Deletion failed: {result}'}, 500
        else:
            return {'message': 'Reminder not found'}, 404

# ==============================================================================
# ⚙️ Admin-Specific Endpoints ⚙️
# ==============================================================================

class AdminUserListResource(Resource):
    def get(self):
        if check_credentials():
            """GET /api/admin/users"""
            # Admin Auth check required
            users = db.get_all_users()
            # Clean data before sending
            user_list = []
            for user in users:
                user_dict = row_to_dict(user)
                # del user_dict['password_hash']
                user_list.append(user_dict)
            return {'users': user_list}, 200
        else:
            return {'error': 'Invalid Credentials'}, 401

class AdminUtilityListResource(Resource):
    def get(self):
        if check_credentials():
            """GET /api/admin/utilities"""
            # Admin Auth check required
            utilities = db.get_all_utilities()
            return {'utilities': [row_to_dict(u) for u in utilities]}, 200
        else:
            return {'error': 'Invalid Credentials'}, 401

class AdminBillListResource(Resource):
    def get(self):
        if check_credentials():
            """GET /api/admin/bills"""
            # Admin Auth check required
            bills = db.get_all_bills()
            # Note: get_all_bills returns a custom join result, so keys are already clean
            return {'bills': [dict(b) for b in bills]}, 200
        else:
            return {'error': 'Invalid Credentials'}, 401

class AdminPaymentListResource(Resource):
    def get(self):
        if check_credentials():
            """GET /api/admin/payments"""
            # Admin Auth check required
            payments = db.get_all_payments()
            # Note: get_all_payments returns a custom join result, so keys are already clean
            return {'payments': [dict(p) for p in payments]}, 200
        else:
            return {'error': 'Invalid Credentials'}, 401
