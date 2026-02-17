# 🚀 Deployment Guide (Docker)

## Prerequisites
- Docker Desktop installed
- Docker Compose enabled
- WSL2 enabled (Windows)

---

## Run Project with Docker

### Step 1: Build & Start Containers
```bash
docker compose up --build
Services
Backend
Runs on port: 8000

MySQL
Runs on port: 3307

API Documentation
Swagger:

http://localhost:8000/docs

Stop Containers
docker compose down
Remove Volumes (Clean Reset)
⚠️ This deletes all database data.

docker compose down -v

---