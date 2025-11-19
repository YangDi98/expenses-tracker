from sqlalchemy import select
from datetime import datetime

from http import HTTPStatus
from src.models.users import User


class TestAuth:
    def test_register(self, client, app, test_db):
        response = client.post(
            "/auth/register",
            json={
                "username": "testuser2",
                "email": "testuser2@example.com",
                "first_name": "Test2",
                "last_name": "User2",
                "password": "password123@AAA",
            },
        )
        assert response.status_code == HTTPStatus.CREATED
        user = test_db.session.execute(
            select(User).where(User.username == "testuser2")
        ).scalar_one_or_none()
        assert user is not None
        assert user.email == "testuser2@example.com"

    def test_register_duplicate_username(self, client, test_user):
        response = client.post(
            "/auth/register",
            json={
                "username": test_user.username,
                "email": "another@example.com",
                "first_name": "Another",
                "last_name": "User",
                "password": "password123@AAA",
            },
        )
        assert response.status_code == HTTPStatus.CONFLICT
        data = response.get_json()
        assert data["message"] == "Username or email already exists"

    def test_register_duplicate_email(self, client, test_user):
        response = client.post(
            "/auth/register",
            json={
                "username": "testuser3",
                "email": test_user.email,
                "first_name": "Another",
                "last_name": "User",
                "password": "password123@AAA",
            },
        )
        assert response.status_code == HTTPStatus.CONFLICT
        data = response.get_json()
        assert data["message"] == "Username or email already exists"

    def test_register_invalid_password(self, client):
        response = client.post(
            "/auth/register",
            json={
                "username": "testuser4",
                "email": "testuser4@example.com",
                "first_name": "Test4",
                "last_name": "User4",
                "password": "short",
            },
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = response.get_json()
        assert "Invalid Password" in data["details"]["json"]["_schema"]

    def test_register_invalid_email(self, client):
        response = client.post(
            "/auth/register",
            json={
                "username": "testuser5",
                "email": "not-an-email",
                "first_name": "Test5",
                "last_name": "User5",
                "password": "password123@AAA",
            },
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = response.get_json()
        assert "Invalid Email Address" in data["details"]["json"]["_schema"]

    def test_register_empty_fields(self, client):
        response = client.post(
            "/auth/register",
            json={
                "username": "   ",
                "email": "   ",
                "first_name": "   ",
                "last_name": "   ",
                "password": "password123@AAA",
            },
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_login_using_email(self, client, test_user):
        response = client.post(
            "/auth/login",
            json={"login": test_user.email, "password": "password123@AAA"},
        )
        assert response.status_code == HTTPStatus.OK
        data = response.get_json()
        cookies = response.headers.getlist("Set-Cookie")
        refresh_cookie_found = any(
            "refresh_token=" in cookie for cookie in cookies
        )
        assert refresh_cookie_found
        assert "access_token" in data

    def test_login_using_username(self, client, test_user):
        response = client.post(
            "/auth/login",
            json={"login": test_user.username, "password": "password123@AAA"},
        )
        assert response.status_code == HTTPStatus.OK
        data = response.get_json()
        cookies = response.headers.getlist("Set-Cookie")
        refresh_cookie_found = any(
            "refresh_token=" in cookie for cookie in cookies
        )
        assert refresh_cookie_found
        assert "access_token" in data

    def test_login_invalid_credentials(self, client, test_user):
        response = client.post(
            "/auth/login",
            json={"login": test_user.email, "password": "wrongpassword"},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        data = response.get_json()
        assert data["message"] == "Invalid credentials"

    def test_login_inactive_account(self, client, test_user, test_db):
        test_user.active = False
        test_db.session.commit()
        response = client.post(
            "/auth/login",
            json={"login": test_user.email, "password": "password123@AAA"},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        data = response.get_json()
        assert data["message"] == "Account is deactivated"

    def test_login_deleted_account(self, client, test_user, test_db):
        test_user.deleted_at = datetime(2024, 1, 1)
        test_db.session.commit()
        response = client.post(
            "/auth/login",
            json={"login": test_user.email, "password": "password123@AAA"},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        data = response.get_json()
        assert data["message"] == "Invalid credentials"

    def test_logout(self, authenticated_client):
        response = authenticated_client.post("/auth/logout")
        assert response.status_code == HTTPStatus.OK
        data = response.get_json()
        assert data["message"] == "Logout successful"
        cookies = response.headers.getlist("Set-Cookie")
        # Check that JWT cookies are being unset (deleted)
        refresh_cookie_deleted = any(
            "refresh_token=" in cookie
            and ("Expires=" in cookie or "Max-Age=0" in cookie)
            for cookie in cookies
        )
        assert refresh_cookie_deleted

    def test_revoked_token_access(self, authenticated_client):
        # Logout to revoke the token
        response = authenticated_client.post("/auth/logout")
        assert response.status_code == HTTPStatus.OK

        # Try to access a protected route with the revoked token
        response = authenticated_client.get("/auth/who_am_i")
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        data = response.get_json()
        assert data["message"] == "Token is not valid"
