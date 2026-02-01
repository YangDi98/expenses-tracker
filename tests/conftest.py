import pytest
import os
from src import create_app
from src.extensions import db
from src.models.users import User

TEST_DB_PATH = "test_expenses_db.sqlite"


class AuthenticatedClient:
    def __init__(self, client, token):
        self.client = client
        self.token = token

    def get(self, *args, **kwargs):
        kwargs.setdefault("headers", {})[
            "Authorization"
        ] = f"Bearer {self.token}"
        return self.client.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        kwargs.setdefault("headers", {})[
            "Authorization"
        ] = f"Bearer {self.token}"
        return self.client.post(*args, **kwargs)

    def patch(self, *args, **kwargs):
        kwargs.setdefault("headers", {})[
            "Authorization"
        ] = f"Bearer {self.token}"
        return self.client.patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        kwargs.setdefault("headers", {})[
            "Authorization"
        ] = f"Bearer {self.token}"
        return self.client.put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        kwargs.setdefault("headers", {})[
            "Authorization"
        ] = f"Bearer {self.token}"
        return self.client.delete(*args, **kwargs)


@pytest.fixture(scope="session")
def app():
    config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.getenv(
            "TEST_DATABASE_URI", f"sqlite:///{TEST_DB_PATH}"
        ),
    }
    app = create_app(config)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="function", autouse=True)
def clean_db(app):
    yield
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()


@pytest.fixture
def test_db(app):
    with app.app_context():
        yield db


@pytest.fixture
def client(app):
    """Return a test client for making requests."""
    return app.test_client()


@pytest.fixture
def test_user(test_db):
    user = User.create(
        data={
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "test@example.com",
        },
        commit=False,
    )
    user.set_password("password123@AAA")
    test_db.session.add(user)
    test_db.session.commit()
    return user


@pytest.fixture
def authenticated_client(client, test_user, app):
    """Return a client already logged in as a test user."""

    response = client.post(
        "/auth/login",
        json={"login": test_user.email, "password": "password123@AAA"},
        follow_redirects=True,
    )
    token = response.get_json()["access_token"]
    return AuthenticatedClient(client, token)
