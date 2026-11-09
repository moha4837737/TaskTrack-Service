import os
import sqlite3

from flask import Flask, jsonify, render_template, request

DB_PATH = os.environ.get("DB_PATH", "tasks.db")
app = Flask(__name__)


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    folder = os.path.dirname(DB_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with db() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS tasks ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title TEXT NOT NULL, "
            "done INTEGER NOT NULL DEFAULT 0)"
        )


init_db()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/api/tasks")
def list_tasks():
    with db() as conn:
        rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])


@app.post("/api/tasks")
def create_task():
    title = ((request.get_json(silent=True) or {}).get("title") or "").strip()
    if not title:
        return jsonify(error="title is required"), 400
    with db() as conn:
        cur = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        task_id = cur.lastrowid
    return jsonify(id=task_id, title=title, done=0), 201


@app.put("/api/tasks/<int:task_id>")
def toggle_task(task_id):
    with db() as conn:
        cur = conn.execute(
            "UPDATE tasks SET done = 1 - done WHERE id = ?", (task_id,)
        )
        if cur.rowcount == 0:
            return jsonify(error="not found"), 404
    return jsonify(id=task_id)


@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    with db() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
