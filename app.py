from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

# Import db from extensions to avoid circular imports
from extensions import db

# Initialize the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-key-that-should-be-changed-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Chidnand Khot/site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_TIME_LIMIT'] = None  # Disable CSRF time limit

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'chidanandkhot03@gmail.com'
app.config['MAIL_PASSWORD'] = ''  # You need to set this with App Password
app.config['MAIL_DEFAULT_SENDER'] = 'chidanandkhot03@gmail.com'

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # This should work, ignoring linter error
login_manager.login_message_category = 'info'

# Import ALL models after initializing extensions to ensure all tables are created
from models.models import User, Admin, Project, Skill, Certificate, Message, Resume, SiteImage, ContactInfo, Education, Experience

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    # Try to load as Admin first for admin users
    admin = Admin.query.get(int(user_id))
    if admin:
        print(f"Loaded admin: {admin.email}")
        return admin
    # If not found, try as User
    user = User.query.get(int(user_id))
    if user:
        print(f"Loaded user: {user.email}")
        return user
    return None

# Initialize database tables
with app.app_context():
    db.create_all()
    # Check if admin user exists, if not create one
    if not Admin.query.first():
        from werkzeug.security import generate_password_hash
        admin = Admin()
        admin.email = 'chidanandkhot03@gmail.com'
        admin.password = generate_password_hash('ChidanandK@3087')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")

# Import routes after initializing app to avoid circular imports
from routes import *