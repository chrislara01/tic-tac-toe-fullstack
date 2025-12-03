# Tic‑Tac‑Toe (Full‑Stack)

A modern full‑stack Tic‑Tac‑Toe game with a React + TypeScript frontend and a FastAPI backend. The backend exposes a clean domain model (Board/Game) with multiple AI strategies (Random, Heuristic, Gemini), and the frontend provides a polished UX with optimistic updates and robust state handling.

## What this project consists of

- Frontend
  - React + TypeScript + Vite
  - SPA routing with React Router
  - Custom hooks for data fetching and game logic
  - Optimistic updates and protection against stale responses
  - Clean separation of concerns between state hooks and presentational components

- Backend
  - FastAPI + Pydantic v2
  - Domain‑driven design: explicit `Board` and `Game` entities
  - AI strategies behind a strategy factory (Random, Heuristic, optional Gemini)
  - Settings via environment variables (dotenv supported)
  - Alembic migrations run automatically at container start
  - CORS configured for the frontend

- DevOps/Infra
  - Docker Compose to build and run frontend and backend
  - Frontend served by Nginx and proxies API to backend
  - You bring your own Postgres (installed manually), then configure backend `.env`

---

## Deployment steps

These steps assume you prefer to install Postgres manually on your machine and then run the web app via Docker Compose.

### 1) Prerequisites

- Docker and Docker Compose
- A local Postgres instance you manage yourself

### 2) Create the database and user in Postgres

Using `psql` (example):

```sql
CREATE USER app_user WITH PASSWORD 'strongpassword';
CREATE DATABASE tictactoe OWNER app_user;
GRANT ALL PRIVILEGES ON DATABASE tictactoe TO app_user;
```

### 3) Configure backend environment

Create `backend/.env` (you can copy from `backend/.env.example` and edit). The important variables:

```env
# Application
APP_NAME=tic-tac-toe-backend
ENVIRONMENT=production
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000

# CORS (adjust if needed, e.g. to your local frontend URL)
CORS_ORIGINS=*

# Database
# On Linux, backend container reaches host Postgres via host.docker.internal (Compose sets the mapping)
DATABASE_URL=postgresql://app_user:strongpassword@host.docker.internal:5432/tictactoe

# Optional: Gemini AI integration
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.0-flash
```

Notes:
- On macOS/Windows `host.docker.internal` generally works by default.
- On Linux we map `host.docker.internal` to the host gateway in `docker-compose.yml` so the backend container can resolve it.

### 4) Start the application with Docker Compose

From the repository root:

```bash
docker compose up --build
```

- The backend entrypoint runs Alembic migrations automatically and starts Uvicorn.
- The frontend is served at http://localhost:80
- The backend API is at http://localhost:8000
  - When accessed through the frontend container, `/api/*` is proxied to the backend.

### 5) Verify health

- Backend health: http://localhost:8000/health
- Frontend should load at http://localhost/

### 6) Alternative local runs (optional)

- Run the backend outside Docker (requires Python 3.13 and uv):

```bash
cd backend
uv sync
cp .env.example .env  # and edit DATABASE_URL accordingly
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Run the frontend outside Docker (requires Node 18+ and your package manager):

```bash
cd frontend
pnpm install  # or npm/yarn
pnpm run dev
```

---

## Architecture and code structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI routers
│   │   ├── core/           # settings, logging, middleware
│   │   ├── db/             # SQLAlchemy models, base
│   │   ├── domain/         # Board, Game, enums, exceptions, AI strategies
│   │   ├── repositories/   # Repository pattern (memory, SQLAlchemy)
│   │   ├── schemas/        # Pydantic models (request/response)
│   │   └── services/       # Application services (GameService)
│   ├── alembic/ (via migrations/)
│   ├── entrypoint.sh       # Migrations + start Uvicorn
│   └── pyproject.toml
└── frontend/
    ├── src/
    │   ├── api/            # client + types
    │   ├── components/
    │   ├── hooks/
    │   ├── pages/
    │   ├── App.tsx, index.css, etc.
    │   └── absolute imports via '@/...'
    ├── vite.config.ts      # '@' alias -> src
    └── tsconfig.app.json   # baseUrl + paths for '@'
```

---

## Highlight of the project

- __Domain‑Driven Design (DDD light)__
  - Clear domain model with `Board` and `Game` encapsulating rules and state transitions.
  - `GameService` orchestrates use cases, decoupled from transport and storage.

- __Strategy Pattern (AI)__
  - `Strategy` interface with multiple implementations:
    - `RandomStrategy` (easy)
    - `HeuristicStrategy` (medium)
    - `GeminiStrategy` (hard, optional external API)
  - `strategy_for()` factory selects a strategy by difficulty.

- __Layered architecture__
  - `api` (transport) → `services` (use cases) → `repositories` (persistence) → `domain` (entities/rules).
  - `schemas` (Pydantic) for API contracts (requests/responses).

- __Robust client state management__
  - Frontend implements optimistic UI and guards against stale/late responses.
  - Derived UI state via `useGameStatus()` and presentation in `StatusBar` for clear separation of concerns.

- __Type safety and DX__
  - Strict TypeScript settings.
  - ESLint + React hooks lint configs.

- __Operational excellence__
  - Dockerized frontend and backend.
  - Alembic migrations run at startup (idempotent).
  - `.env` driven configuration using Pydantic settings + dotenv.
  - Nginx proxies `/api` to backend for a clean deployment surface.

- __Security and reliability touches__
  - CORS configured via envs.
  - Defensive parsing and error handling on both client and server.
  - Graceful fallback in Gemini strategy when API or SDK is unavailable.

- __Accessibility and UX__
  - `aria-live` for status updates.
  - Clear status messages for error/win/draw/in‑progress states.

---

## API overview (brief)

- `GET /health` — Health check.
- `POST /games` — Create a game.
- `GET /games/{id}` — Fetch a game.
- `POST /games/{id}/moves` — Submit a move.

Pydantic models in `backend/app/schemas/` define request/response contracts.

---

## Local development tips

- Backend in Docker reaching host Postgres uses `host.docker.internal` which is mapped in `docker-compose.yml`.
- If you change TypeScript path aliases or Vite config, restart the dev server.
- If you modify DB models, create a migration and it will apply at startup:

```bash
cd backend
uv run alembic revision -m "add something"
uv run alembic upgrade head
```

---

## License

This project is for demonstration and educational purposes.
