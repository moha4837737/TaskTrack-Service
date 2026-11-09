# TaskTrack-Service

A small task manager with a REST API and a simple web UI. Add tasks, mark them done, delete them. Data is stored in SQLite and persisted in a Docker volume.

## Tech Stack
Python 3.12 · Flask · Gunicorn · SQLite · Docker (multi-stage) · Docker Compose · GitHub Actions

## Run with Docker
```bash
git clone https://github.com/Mohammed/TaskTrack-Service.git
cd TaskTrack-Service
docker build -t TaskTrack-Service .
docker run -d --name TaskTrack-Service -p 5000:5000 -v tasks-data:/data TaskTrack-Service
```
Or with Docker Compose: `docker compose up -d --build`
Or with Make: `make build && make run`

## Test it
- UI: open http://localhost:5000
- Health: `curl http://localhost:5000/health` → `{"status":"ok"}`
- API:
```bash
curl -X POST http://localhost:5000/api/tasks -H "Content-Type: application/json" -d '{"title":"Learn Docker"}'
curl http://localhost:5000/api/tasks
```
- Unit tests (locally): `make test`

## Stop and clean up
```bash
docker stop TaskTrack-Service && docker rm TaskTrack-Service   # or: docker compose down
docker volume rm tasks-data                            # deletes saved data
docker rmi TaskTrack-Service                               # removes the image
```

## Configuration
| Variable | Default | Meaning |
|----------|---------|---------|
| `DB_PATH` | `/data/tasks.db` | SQLite file location inside the container |
| Port | `5000` | Change the left side of `-p 5000:5000` to use another host port |

## API
| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/tasks` | List tasks |
| POST | `/api/tasks` | Create task `{"title": "..."}` |
| PUT | `/api/tasks/<id>` | Toggle done |
| DELETE | `/api/tasks/<id>` | Delete task |

## Attribution
Original project written from scratch for this assignment. No third-party code base was used.
