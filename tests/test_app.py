import os
import sys
import tempfile

os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app import app  # noqa: E402

client = app.test_client()


def test_health():
    assert client.get("/health").get_json() == {"status": "ok"}


def test_task_lifecycle():
    r = client.post("/api/tasks", json={"title": "Write README"})
    assert r.status_code == 201
    task_id = r.get_json()["id"]
    assert client.put(f"/api/tasks/{task_id}").status_code == 200
    tasks = client.get("/api/tasks").get_json()
    assert tasks[0]["done"] == 1
    assert client.delete(f"/api/tasks/{task_id}").status_code == 204


def test_empty_title_rejected():
    assert client.post("/api/tasks", json={"title": " "}).status_code == 400
