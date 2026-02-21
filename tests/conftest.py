import pytest
from app import create_app, db

@pytest.fixture
def app():
    # testing mode
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:" # temporary db
    })
    
    # create tables -> run tests -> drop tables
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()