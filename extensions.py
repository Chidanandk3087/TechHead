from flask_sqlalchemy import SQLAlchemy

# Create a global db instance to avoid circular imports
db = SQLAlchemy()