from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    # Arrange
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_new_participant():
    # Arrange
    email = "test_new_user@example.com"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json().get("message", "")

    # Re-check state
    list_response = client.get("/activities")
    assert list_response.status_code == 200
    participants = list_response.json()[activity]["participants"]
    assert email in participants


def test_signup_duplicate_participant():
    # Arrange
    email = "test_dup_user@example.com"
    activity = "Chess Club"

    # Act
    first = client.post(f"/activities/{activity}/signup?email={email}")
    second = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert first.status_code == 200
    assert second.status_code == 400
    assert "already signed up" in second.json().get("detail", "")


def test_unregister_participant():
    # Arrange
    email = "test_unregister_user@example.com"
    activity = "Chess Club"

    # Add first so remove works
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json().get("message", "")

    # Verify removed
    list_response = client.get("/activities")
    assert list_response.status_code == 200
    participants = list_response.json()[activity]["participants"]
    assert email not in participants


def test_unregister_nonexistent_participant():
    # Arrange
    email = "nonexistent_user@example.com"
    activity = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json().get("detail", "")
