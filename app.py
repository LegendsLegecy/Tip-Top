from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import random
from datetime import datetime
from flask_mail import Mail, Message
from config import config

app = Flask(__name__)
app.config.from_object(config['default'])

# File upload configuration
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signup'
mail = Mail(app)

# Register blueprints
from admin_routes import admin_bp
app.register_blueprint(admin_bp)

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False, cascade='all, delete-orphan')

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coins = db.Column(db.Integer, default=0)
    money = db.Column(db.Numeric(10, 2), default=0.00)

class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email(to_email, subject, html_content, text_content):
    try:
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to_email])
        msg.html = html_content
        msg.body = text_content
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

# Routes
@app.route('/')
def index():
    return redirect(url_for('signup'))

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Sign up fields
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Login fields
        loginemail = request.form.get('login-email')
        loginpassword = request.form.get('login-password')

        # ---- SIGNUP logic ----
        if username and email and password1 and password2 and not loginemail and not loginpassword:
            if password1 != password2:
                flash("Passwords do not match.", "error")
            elif User.query.filter_by(username=username).first():
                flash("Username already exists.", "error")
            elif User.query.filter_by(email=email).first():
                flash("Email already exists.", "error")
            else:
                user = User(
                    username=username,
                    email=email,
                    password_hash=generate_password_hash(password1)
                )
                db.session.add(user)
                db.session.commit()
                
                # Create profile for the user
                profile = Profile(user_id=user.id)
                db.session.add(profile)
                db.session.commit()
                
                flash("Signup successful! You can now log in.", "success")
                return redirect(url_for('signup'))

        # ---- LOGIN logic ----
        elif loginemail and loginpassword and not username and not email and not password1 and not password2:
            user = User.query.filter_by(email=loginemail).first()
            if user and check_password_hash(user.password_hash, loginpassword):
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid credentials.", "error")
        else:
            flash("Invalid form submission.", "error")

    return render_template('signup.html')

@app.route('/logout/')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('signup'))

@app.route('/dashboard/')
@login_required
def dashboard():
    try:
        profile = current_user.profile
        data = {
            "usrname": current_user.username,
            "coins": profile.coins if profile else 0,
            "money": float(profile.money) if profile else 0.00
        }
    except AttributeError:
        data = {
            "usrname": current_user.username,
            "coins": 0,
            "money": 0.00
        }
    return render_template("dashboard.html", **data)

@app.route('/earn-coins/')
@login_required
def earn_coins():
    try:
        profile = current_user.profile
        if profile:
            profile.coins += 10
            db.session.commit()
            flash("You earned 10 coins!", "success")
        else:
            flash("Profile not found. Please contact support.", "error")
    except Exception as e:
        flash("Error earning coins.", "error")
    return redirect(url_for('dashboard'))

@app.route('/redeem-coins/')
@login_required
def redeem_coins():
    try:
        profile = current_user.profile
        if profile and profile.coins >= 100:
            profile.coins -= 100
            profile.money += 1
            db.session.commit()
            flash("You redeemed 100 coins for $1!", "success")
        else:
            flash("Not enough coins to redeem.", "error")
    except Exception as e:
        flash("Error redeeming coins.", "error")
    return redirect(url_for('dashboard'))

@app.route('/coin-price-graph/')
@login_required
def coin_price_graph():
    try:
        profile = current_user.profile
        data = {
            "usrname": current_user.username,
            "coins": profile.coins if profile else 0,
            "money": float(profile.money) if profile else 0.00
        }
    except AttributeError:
        data = {
            "usrname": current_user.username,
            "coins": 0,
            "money": 0.00
        }
    return render_template("coins/coin_price_graph.html", **data)

@app.route('/ads/')
def ads_list():
    ads = Ad.query.filter_by(is_active=True).order_by(Ad.created_at.desc()).limit(10).all()
    return render_template("ads/ads_list.html", ads=ads)

@app.route('/forgot-password/', methods=['GET', 'POST'])
def forgot_password():
    if request.method == "POST":
        if 'email' in request.form:
            email = request.form.get("email")
            user = User.query.filter_by(email=email).first()
            
            if user:
                verification_code = str(random.randint(100000, 999999))
                session['verification_code'] = verification_code
                session['reset_email'] = email

                # Render HTML email
                html_content = render_template('reset-pass-mail.html', 
                                            username=user.username, 
                                            code=verification_code)
                text_content = f"Your verification code is: {verification_code}"
                
                if send_email(email, "Password Reset Verification Code", html_content, text_content):
                    flash("Verification code has been sent to your email.", "success")
                else:
                    flash("Failed to send email. Please try again.", "error")
            else:
                flash("Email not found in our system.", "error")

        elif 'code' in request.form:
            entered_code = request.form.get("code")
            saved_code = session.get("verification_code")

            if entered_code == saved_code:
                flash("Code verified! You can now reset your password.", "success")
                return redirect(url_for("reset_password"))
            else:
                flash("Invalid verification code.", "error")

    return render_template("forgot-password.html")

@app.route('/reset-password/', methods=['GET', 'POST'])
def reset_password():
    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        email = session.get("reset_email")

        if not email:
            flash("Session expired. Please try again.", "error")
            return redirect(url_for("forgot_password"))

        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("reset_password"))

        try:
            user = User.query.filter_by(email=email).first()
            if user:
                user.password_hash = generate_password_hash(new_password)
                db.session.commit()

                # Clear session data
                session.pop('verification_code', None)
                session.pop('reset_email', None)

                flash("Password has been reset successfully.", "success")
                return redirect(url_for("signup"))
            else:
                flash("User not found.", "error")
                return redirect(url_for("signup"))

        except Exception as e:
            flash("Error resetting password.", "error")
            return redirect(url_for("login"))

    return render_template("reset-password.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
