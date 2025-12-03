#!/usr/bin/env sh
set -e

# Run database migrations (idempotent)
echo "[entrypoint] Running Alembic migrations..."
uv run alembic upgrade head

# Start the FastAPI app
echo "[entrypoint] Starting Uvicorn..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
