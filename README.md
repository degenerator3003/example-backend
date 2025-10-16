# Example Backend — FastAPI + PostgreSQL + Alembic + Docker Compose

A production-grade backend template built with **FastAPI**, **SQLAlchemy**, **Alembic**, and **PostgreSQL**, containerized via **Docker Compose**.

---

## 🚀 Overview

This backend provides a minimal but complete trading API demonstration including:

- Organisations, customers, currencies, goods, and inventory management.
- Documents for **buy/sell** operations that automatically adjust inventory.
- Transactional activation/deactivation of documents.
- Database migrations using **Alembic**.
- Easy first-run seeding with example data.
- HTTPS-ready local setup.

---

## 🧱 Tech Stack

| Component | Purpose |
|------------|----------|
| **FastAPI** | Web framework for the REST API |
| **SQLAlchemy 2.0** | ORM and database engine |
| **Alembic** | Schema migrations |
| **PostgreSQL** | Persistent relational database |
| **Docker Compose** | Multi-service orchestration |
| **Pydantic v2** | Validation and settings management |

---

## ⚙️ Project Structure

```
example-backend/
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── requirements.txt
│   └── app/
│       ├── core/          # config.py, db.py
│       ├── models/        # SQLAlchemy ORM models
│       ├── repositories/  # CRUD/data access logic
│       ├── routes/        # API endpoints
│       ├── seed.py        # initial data population
│       └── main.py        # FastAPI entrypoint
```

---

## 🧩 Environment Configuration

Duplicate `.env.example` as `.env` and adjust parameters if necessary:

```bash
cp .env.example .env
```

`.env` example:

```env
POSTGRES_DB=tradedb
POSTGRES_USER=trade
POSTGRES_PASSWORD=tradepw
DATABASE_URL=postgresql+psycopg2://trade:tradepw@db:5432/tradedb
SEED_ON_START=true
```

---

## 🐳 Run with Docker Compose

Build and launch:

```bash
docker compose up --build
```

The API becomes available at:

```
https://localhost:8443/
```

> ⚠️ Self-signed certificates are generated automatically for local HTTPS.

List all logs:

```bash
docker compose logs -f
```

Stop containers:

```bash
docker compose down
```

---

## 🧰 Local Development (Virtualenv)

You can also run the backend directly on your host:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
export DATABASE_URL="postgresql+psycopg2://trade:tradepw@localhost:5432/tradedb"
alembic upgrade head
python backend/app/seed.py
uvicorn backend.app.main:app --reload
```

The API runs on:
```
http://127.0.0.1:8000
```

---

## 🔄 Database Migrations (Alembic)

Initialize Alembic once:

```bash
cd backend
alembic init migrations
```

Edit `migrations/env.py` to load environment variables before importing `engine`:

```python
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[2] / ".env")
from app.core.db import engine, Base
target_metadata = Base.metadata
```

Create new migration after changing models:

```bash
alembic revision --autogenerate -m "update schema"
```

Apply migrations:

```bash
alembic upgrade head
```

---

## 🧪 Example API Usage

Health check:
```bash
curl -k https://localhost:8443/
```

List goods:
```bash
curl -k https://localhost:8443/api/goods/
```

Activate a document (example ID = 1):
```bash
curl -k -X POST https://localhost:8443/api/documents/1/activate \
  -H 'Content-Type: application/json' -d '{"active": true}'
```

Deactivate (rollback stock):
```bash
curl -k -X POST https://localhost:8443/api/documents/1/activate \
  -H 'Content-Type: application/json' -d '{"active": false}'
```

---

## 🧾 Seeding Example Data

On first start, seed data will populate automatically if `SEED_ON_START=true`.

To rerun manually:

```bash
docker compose exec api python -m app.seed
```

---

## 🧠 Development Notes

- Alembic handles schema migrations — **never edit the DB manually**.
- When running in host venv, use `localhost`; inside Docker use `db` as hostname.
- Enforce uniqueness constraints in models to prevent data duplication.
- Use `docker compose logs api | less` to view full application logs.

---

## 📘 API Summary

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/api/parties/organisations` | GET / POST | Manage organisations |
| `/api/parties/customers` | GET / POST | Manage customers |
| `/api/parties/currencies` | GET / POST | Manage currencies |
| `/api/goods/` | GET / POST | Manage goods |
| `/api/goods/inventory` | GET | Check stock levels |
| `/api/documents/` | GET / POST | Manage trade documents |
| `/api/documents/{id}/activate` | POST | Apply or revert inventory |

---

## 🧩 Troubleshooting

| Problem | Likely Cause | Fix |
|----------|---------------|-----|
| `ValidationError: database_url` | Missing DATABASE_URL in .env | Check `.env` path and variable name |
| `transaction already begun` | Nested transaction in FastAPI session | Remove `with db.begin()` and use `db.commit()` |
| `Multiple rows were found...` | Duplicate document numbers | Enforce unique constraint on `doc_num` |

---

© 2025 Example Backend — FastAPI Trade Service Template
