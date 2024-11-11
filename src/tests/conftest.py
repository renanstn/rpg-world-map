import pytest

from app import app, db


@pytest.fixture
def client():
    # Create tables when client init
    with app.app_context():
        db.create_all()

    # Serve test client instance
    with app.test_client() as client:
        yield client

    # Drop tables when client finish
    with app.app_context():
        db.drop_all()
