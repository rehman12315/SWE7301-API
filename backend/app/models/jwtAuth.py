"""
US-13: Authentication and Protected Routes
US-16: JWTs via Website
"""
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
import datetime

# Simple in-memory user storage for demo (replace with real database in production)
USERS = {
    "admin": {"password": "password", "email": "admin@geoscope.com", "first_name": "Admin", "last_name": "User"}
}

def register(app):
    """
    Registers authentication routes with JWT support for US-16.
    """
    
    @app.route('/login', methods=['POST'])
    def login():
        try:
            username = request.json.get("username")
            password = request.json.get("password")
            
            # Check against registered users or hardcoded admin
            user_data = None
            if username == "admin" and password == "password":
                user_data = USERS["admin"]
            elif username in USERS and USERS[username]["password"] == password:
                user_data = USERS[username]
            else:
                return jsonify({"msg": "Bad username or password"}), 401

            # Create access and refresh tokens
            access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(hours=1))
            refresh_token = create_refresh_token(identity=username, expires_delta=datetime.timedelta(days=30))
            
            return jsonify({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "username": username,
                    "email": user_data.get("email", ""),
                    "first_name": user_data.get("first_name", ""),
                    "last_name": user_data.get("last_name", "")
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/signup', methods=['POST'])
    def signup():
        try:
            data = request.json
            first_name = data.get("first_name")
            last_name = data.get("last_name") 
            email = data.get("email")
            password = data.get("password")
            
            if not all([first_name, last_name, email, password]):
                return jsonify({"message": "All fields are required"}), 400
                
            # Check if user already exists
            if email in USERS:
                return jsonify({"message": "User already exists"}), 409
                
            # Store user (in real app, hash password)
            USERS[email] = {
                "password": password,
                "email": email,
                "first_name": first_name,
                "last_name": last_name
            }
            
            return jsonify({"message": "User created successfully"}), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():
        """Refresh expired access token - US-16 requirement"""
        try:
            current_user = get_jwt_identity()
            new_token = create_access_token(identity=current_user, expires_delta=datetime.timedelta(hours=1))
            return jsonify({
                "access_token": new_token,
                "msg": "Token refreshed successfully"
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/token/validate', methods=['POST'])
    @jwt_required()
    def validate_token():
        """Validate current JWT token - US-16 requirement"""
        try:
            current_user = get_jwt_identity()
            jwt_data = get_jwt()
            return jsonify({
                "valid": True,
                "user": current_user,
                "exp": jwt_data.get("exp"),
                "msg": "Token is valid"
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        try:
            current_user = get_jwt_identity()
            return jsonify({
                "msg": "Given valid token, when used, then data returned.",
                "user": current_user,
                "data": "Top Secret Info"
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
