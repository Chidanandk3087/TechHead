from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Import db from a separate module to avoid circular imports
from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def __repr__(self):
        return f"Admin('{self.email}')"

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    link = db.Column(db.String(200), nullable=True)
    
    def __repr__(self):
        return f"Project('{self.title}')"

class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(20), nullable=False, default='default.png')
    image = db.Column(db.String(100), nullable=True)  # Add image field
    
    def __repr__(self):
        return f"Skill('{self.name}')"

class Certificate(db.Model):
    __tablename__ = 'certificates'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    def __repr__(self):
        return f"Certificate('{self.title}')"

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Message('{self.name}', '{self.date}')"

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Resume('{self.filename}', '{self.upload_date}')"

class SiteImage(db.Model):
    __tablename__ = 'site_images'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # e.g., 'profile', 'home_hero', 'about_banner'
    filename = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"SiteImage('{self.name}', '{self.filename}')"

class ContactInfo(db.Model):
    __tablename__ = 'contact_info'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    map_embed_url = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f"ContactInfo('{self.email}')"

class Education(db.Model):
    __tablename__ = 'education'
    
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(200), nullable=False)
    institution = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)  # e.g., "2018"
    end_date = db.Column(db.String(20), nullable=False)    # e.g., "2022" or "Present"
    description = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, nullable=False, default=0)  # For ordering
    image = db.Column(db.String(100), nullable=True)  # Image filename
    
    def __repr__(self):
        return f"Education('{self.degree}', '{self.institution}')"

class Experience(db.Model):
    __tablename__ = 'experience'
    
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)  # e.g., "2022"
    end_date = db.Column(db.String(20), nullable=False)    # e.g., "2023" or "Present"
    description = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, nullable=False, default=0)  # For ordering
    
    def __repr__(self):
        return f"Experience('{self.position}', '{self.company}')"
