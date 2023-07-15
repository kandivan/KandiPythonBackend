from flask import Flask, request, jsonify, make_response, abort, render_template, redirect, url_for, redirect
from flask_login import login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash
from auth import authenticate, authorize, login_manager, check_password_hash, login_user, logout_user, current_user,  LoginForm, RegisterForm, load_user
from database import Database, User
from events import EventSystem
from telemetry import Telemetry
from dashboard import Dashboard
from ai_generation import AIGenerationService

app = Flask(__name__)
app.secret_key = 'this_is_a_secret_key'  # Secret key for Flask-Login sessions

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

# Initialize Flask-Login
login_manager.init_app(app)
login_manager.login_view = 'login'
# Initialize database connection
db = Database()
session = db.get_session()

# Initialize event system
event_system = EventSystem()

# Initialize telemetry
telemetry = Telemetry(db, event_system)

# Initialize dashboard
dashboard = Dashboard(db)

ai_service = AIGenerationService()

# Routes
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data, 10).decode('utf-8')
        print(hashed_password)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        session.add(new_user)
        session.commit()
        return redirect(url_for('login'))
    
    return render_template('registration.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(username=form.username.data).first()
        if user:
            try:
                new_generated_password_hash = bcrypt.generate_password_hash(form.password.data)
                print(new_generated_password_hash)
                print(user.password)
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('dashboard'))
                else:
                    return "Invalid login credentials."
            except:
                return "Invalid login credentials."
    
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/dashboard")
@login_required
def get_dashboard():
    return render_template('dashboard.html')
    dashboard_data = dashboard.fetch_data()
    if not dashboard_data:
        abort(500, description="Error fetching dashboard data.")
    return jsonify(dashboard_data)



@app.route("/ai-generate", methods=["POST"])
def ai_generate():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        abort(400, description="No prompt provided.")
    generated_text = ai_service.generate_text(prompt)
    return jsonify({"generated_text": generated_text})

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
    app.run(port=5001, debug=True)
