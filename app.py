from flask import Flask, request, jsonify, make_response, abort
from flask_login import login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from auth import authenticate, authorize, login_manager
from database import Database
from events import EventSystem
from telemetry import Telemetry
from dashboard import Dashboard

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Secret key for Flask-Login sessions

# Initialize Flask-Login
login_manager.init_app(app)

# Initialize database connection
db = Database()

# Initialize event system
event_system = EventSystem()

# Initialize telemetry
telemetry = Telemetry(db, event_system)

# Initialize dashboard
dashboard = Dashboard(db)

# Routes
@app.route("/")
def home():
    return "Welcome to the API"

@app.route("/login", methods=["POST"])
@authenticate
def login():
    if not current_user.is_authenticated:
        abort(401)
    return jsonify({"message": f"Logged in as {current_user.username}."})

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out."})

@app.route("/dashboard")
@login_required
def get_dashboard():
    dashboard_data = dashboard.fetch_data()
    if not dashboard_data:
        abort(500, description="Error fetching dashboard data.")
    return jsonify(dashboard_data)

# Other API routes...

# Error handlers...
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad request", "message": str(e)}), 400

@app.errorhandler(401)
def unauthorized(e):
    return jsonify({"error": "Unauthorized", "message": str(e)}), 401

@app.errorhandler(403)
def forbidden(e):
    return jsonify({"error": "Forbidden", "message": str(e)}), 403

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found", "message": str(e)}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Internal server error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
