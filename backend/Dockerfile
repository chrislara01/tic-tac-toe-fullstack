# syntax=docker/dockerfile:1

FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:${PATH}" \
    UV_LINK_MODE=copy

# System deps for building wheels (psycopg2) and installing uv
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv (Astral's package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app

# Copy project metadata first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies into a local virtualenv managed by uv
RUN uv sync --no-dev

# Copy the rest of the backend source
COPY . .

EXPOSE 8000

# Entrypoint handles migrations then starts FastAPI
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
