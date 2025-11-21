import pytest
from http import HTTPStatus


class TestExpenses:
    @pytest.fixture(scope="function", autouse=True)
    def setup_expense_category(self, authenticated_client, test_user):
        # Create a category for the user to use in expense creation
        response = authenticated_client.post(
            f"/users/{test_user.id}/categories/",
            json={"name": "Food", "description": "Food related expenses"},
        )
        assert response.status_code == HTTPStatus.CREATED
        data = response.get_json()
        yield data["id"]

    def test_create_expense(
        self, authenticated_client, test_user, setup_expense_category
    ):
        response = authenticated_client.post(
            f"/users/{test_user.id}/expenses/",
            json={
                "amount": 50.0,
                "note": "Grocery shopping",
                "category_id": setup_expense_category,
            },
        )
        assert response.status_code == HTTPStatus.CREATED
        data = response.get_json()
        assert data["amount"] == 50.0
        assert data["note"] == "Grocery shopping"
        assert data["category_id"] == setup_expense_category
        assert data["user_id"] == test_user.id

    def test_get_expenses(
        self, authenticated_client, test_user, setup_expense_category
    ):
        # Create an expense via HTTP request
        response = authenticated_client.post(
            f"/users/{test_user.id}/expenses/",
            json={
                "amount": 50.0,
                "note": "Grocery shopping",
                "category_id": setup_expense_category,
            },
        )
        assert response.status_code == HTTPStatus.CREATED

        response = authenticated_client.get(f"/users/{test_user.id}/expenses/")
        assert response.status_code == HTTPStatus.OK
        data = response.get_json()
        assert "data" in data
        assert len(data["data"]) > 0

    def test_get_expense_by_id(
        self, authenticated_client, test_user, setup_expense_category
    ):
        post_response = authenticated_client.post(
            f"/users/{test_user.id}/expenses/",
            json={
                "amount": 50.0,
                "note": "Grocery shopping",
                "category_id": setup_expense_category,
            },
        )
        expense_id = post_response.get_json()["id"]
        get_response = authenticated_client.get(
            f"/users/{test_user.id}/expenses/{expense_id}"
        )
        assert get_response.status_code == HTTPStatus.OK
        data = get_response.get_json()
        assert data["id"] == expense_id

    def test_update_expense(
        self, authenticated_client, test_user, setup_expense_category
    ):
        post_response = authenticated_client.post(
            f"/users/{test_user.id}/expenses/",
            json={
                "amount": 50.0,
                "note": "Grocery shopping",
                "category_id": setup_expense_category,
            },
        )
        expense_id = post_response.get_json()["id"]
        put_response = authenticated_client.put(
            f"/users/{test_user.id}/expenses/{expense_id}",
            json={
                "amount": 75.0,
                "note": "Updated grocery shopping",
            },
        )
        assert put_response.status_code == HTTPStatus.OK
        data = put_response.get_json()
        assert data["amount"] == 75.0
        assert data["note"] == "Updated grocery shopping"

    def test_get_expenses_pagination(
        self, authenticated_client, test_user, setup_expense_category
    ):
        # Create multiple expenses to test pagination
        for i in range(15):
            authenticated_client.post(
                f"/users/{test_user.id}/expenses/",
                json={
                    "amount": 10.0 + i,
                    "note": f"Expense {i}",
                    "category_id": setup_expense_category,
                },
            )
        response = authenticated_client.get(
            f"/users/{test_user.id}/expenses/?limit=10"
        )
        assert response.status_code == HTTPStatus.OK
        data = response.get_json()
        assert "data" in data
        assert len(data["data"]) == 10
        assert "next_url" in data
        assert data["next_url"] is not None

    def test_create_expense_invalid_category(
        self, authenticated_client, test_user, setup_expense_category
    ):
        response = authenticated_client.post(
            f"/users/{test_user.id}/expenses/",
            json={
                "amount": 50.0,
                "note": "Grocery shopping",
                "category_id": 999,  # Non-existent category
            },
        )
        assert response.status_code == HTTPStatus.NOT_FOUND
        data = response.get_json()
        assert data["message"] == "The requested resource was not found"
