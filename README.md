# AgentScale Control Plane (ACP)

## ACP Gateway (FastAPI)

A minimal FastAPI gateway with:

- Health checks  
- Postgres DB connectivity  
- API-key protected route  
- Redis-backed rate limiting  
- Local infra via Docker Compose (Postgres + Redis)

---

## Project Structure

```text
acp/
├─ apps/
│  └─ gateway/
│     ├─ app/
│     │  ├─ main.py
│     │  ├─ db.py
│     │  ├─ models.py
│     │  ├─ auth.py
│     │  ├─ redis_client.py
│     │  ├─ ratelimit.py
│     │  ├─ seed.py
│     │  └─ set_limit.py
│     ├─ requirements.txt
│     └─ .env
├─ infra/
│  └─ docker-compose.yml
└─ README.md

## How to run locally

### 1) Start infra (Postgres + Redis)
```bash
cd infra
docker compose up -d
docker ps
