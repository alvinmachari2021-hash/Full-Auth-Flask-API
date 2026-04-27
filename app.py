# app.py
from flask import Flask
from config import Config

# Import extensions from a single source of truth
from extensions import db, migrate, bcrypt, jwt

def create_app():
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from routes import auth_bp, notes_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(notes_bp, url_prefix="/notes")

    return app

# Run the app directly (development mode)
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
