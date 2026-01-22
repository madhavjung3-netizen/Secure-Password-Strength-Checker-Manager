from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from . import db, bcrypt
from .models import User, PasswordEntry
from .security_utils import check_password_strength, check_have_i_been_pwned
import pyotp
import qrcode
import io
import base64

main = Blueprint('main', __name__)

# --- AUTHENTICATION ROUTES ---

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user already exists BEFORE creating them
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            flash('Username or Email already exists. Please choose another or login.', 'danger')
            return redirect(url_for('main.register'))

        # Hash password securely
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Generate 2FA Secret
        totp_secret = pyotp.random_base32()
        
        new_user = User(username=username, email=email, password_hash=hashed_pw, totp_secret=totp_secret)
        db.session.add(new_user)
        db.session.commit()
        
        # FIX: Refresh the user instance to ensure the ID is populated from the DB
        # This prevents the "BuildError" where user_id is None
        db.session.refresh(new_user)
        
        # Show 2FA QR Code immediately
        return redirect(url_for('main.setup_2fa', user_id=new_user.id))
    return render_template('register.html')

@main.route('/setup_2fa/<int:user_id>')
def setup_2fa(user_id):
    user = db.session.get(User, user_id)
    # Create QR Code
    uri = pyotp.totp.TOTP(user.totp_secret).provisioning_uri(name=user.email, issuer_name="SecurePassManager")
    img = qrcode.make(uri)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return render_template('setup_2fa.html', qr_code=img_str, secret=user.totp_secret)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        token = request.form.get('2fa_token') # The 6-digit code
        
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            # Verify 2FA
            totp = pyotp.TOTP(user.totp_secret)
            # Verify allowing for a slight time drift (validating previous/next 30s window)
            if totp.verify(token, valid_window=1): 
                login_user(user)
                return redirect(url_for('main.dashboard'))
            else:
                flash('Invalid 2FA Token', 'danger')
        else:
            flash('Login Failed. Check credentials.', 'danger')
            
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# --- APP FEATURES ---

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@main.route('/checker', methods=['GET', 'POST'])
@login_required
def checker():
    result = None
    pwned_status = None
    
    if request.method == 'POST':
        password = request.form.get('password')
        result = check_password_strength(password)
        pwned_status = check_have_i_been_pwned(password)
        
    return render_template('checker.html', result=result, pwned_status=pwned_status)
