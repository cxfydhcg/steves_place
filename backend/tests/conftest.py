import pytest
import sys
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from db import db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create the app with testing config
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False
    })
    
    # Create the database and the database table
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def db_session(app):
    """Create a database session for testing."""
    with app.app_context():
        yield db.session
    

@pytest.fixture
def configure_logging():
    """Configure logging for tests."""
    logging.basicConfig(level=logging.INFO)
    yield
    logging.getLogger().handlers = []
    logging.getLogger().setLevel(logging.NOTSET)
    logging.getLogger('werkzeug').handlers = []
    logging.getLogger('werkzeug').setLevel(logging.NOTSET)