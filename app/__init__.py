from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

#Using an app factory to keep the code modular - organized, scalable, testing and maintainability - for Flask web framework

def create_app():
    app = Flask(__name__)
    
    # Load the database URL from the .env file
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from . import models  #Loading database tables
        # We will register our API routes here next
        
    return app