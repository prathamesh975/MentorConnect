import pytest

from app import app, mentors, mentorship_requests


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

    mentorship_requests.clear()


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_mentors_api(client):
    response = client.get("/api/mentors")

    assert response.status_code == 200

    data = response.get_json()

    assert "mentors" in data
    assert len(data["mentors"]) == 3


def test_valid_mentorship_request(client):
    response = client.post(
        "/request",
        data={
            "student_name": "Test Student",
            "mentor_id": "1",
            "topic": "Machine Learning",
            "message": "I need guidance with ML."
        }
    )

    assert response.status_code == 302
    assert len(mentorship_requests) == 1
    assert mentorship_requests[0]["status"] == "Pending"


def test_invalid_empty_request(client):
    response = client.post(
        "/request",
        data={
            "student_name": "",
            "mentor_id": "",
            "topic": "",
            "message": ""
        }
    )

    assert response.status_code == 200
    assert len(mentorship_requests) == 0


def test_invalid_mentor(client):
    response = client.post(
        "/request",
        data={
            "student_name": "Test Student",
            "mentor_id": "999",
            "topic": "Machine Learning",
            "message": "I need guidance."
        }
    )

    assert response.status_code == 200
    assert len(mentorship_requests) == 0


def test_update_request_status(client):
    client.post(
        "/request",
        data={
            "student_name": "Test Student",
            "mentor_id": "1",
            "topic": "Machine Learning",
            "message": "I need guidance."
        }
    )

    response = client.post(
        "/requests/1/status",
        data={
            "status": "Accepted"
        }
    )

    assert response.status_code == 302
    assert mentorship_requests[0]["status"] == "Accepted"


def test_unavailable_mentor(client):
    original_slots = mentors[0]["slots"]
    mentors[0]["slots"] = 0

    response = client.post(
        "/request",
        data={
            "student_name": "Test Student",
            "mentor_id": "1",
            "topic": "Machine Learning",
            "message": "I need guidance."
        }
    )

    assert response.status_code == 200
    assert len(mentorship_requests) == 0

    mentors[0]["slots"] = original_slots
