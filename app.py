import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app():
    # Create the app
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-pancake-cinema")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///workflow.db")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize the app with the extension
    db.init_app(app)
    
    with app.app_context():
        # Import models to ensure tables are created
        import models
        db.create_all()
        
        # Register blueprints
        from routes.auth import auth_bp
        from routes.workflow import workflow_bp
        from routes.profile import profile_bp
        
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(workflow_bp, url_prefix='/workflow')
        app.register_blueprint(profile_bp, url_prefix='/profile')
        
        # Root route
        @app.route('/')
        def index():
            from flask import session, redirect, url_for, render_template
            if 'user_id' in session:
                return redirect(url_for('workflow.dashboard'))
            return render_template('login.html')
    
    return app

# Create the app instance
app = create_app()
