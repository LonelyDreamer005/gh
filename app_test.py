from app import app

client = app.test_client()


def test_home():
    res = client.get("/")
    assert res.status_code == 200


def test_get_students():
    res = client.get("/students")
    assert res.status_code == 200


def test_add_student():
    res = client.post("/students", json={"name": "Alice", "course": "CS"})
    assert res.status_code == 201
