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

## Test Rate Limiting

1) Set RPM limit (example: 10)
```bash
cd apps/gateway
python -m app.set_limit

# 2) Run API (new terminal)
cd apps/gateway
.\.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000

# 3) Check health
curl http://127.0.0.1:8000/health

# 4) Test protected route (PowerShell)
Invoke-WebRequest -Uri "http://127.0.0.1:8000/protected" -Headers @{Authorization="Bearer demo-secret-key"} -UseBasicParsing

# 5) Rate-limit test (30 hits)
for ($i=1; $i -le 30; $i++) {
  $code = (Invoke-WebRequest -Uri "http://127.0.0.1:8000/protected" -Headers @{Authorization="Bearer demo-secret-key"} -UseBasicParsing).StatusCode
  "$i -> $code"
}

