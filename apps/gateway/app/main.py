from app.redis_client import redis_client
from app.ratelimit import enforce_rpm

from fastapi import Header, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.auth import require_api_key

from fastapi import FastAPI
from app.db import test_db_connection, engine
from app.models import Base

app = FastAPI(title="ACP Gateway", version="0.1.0")
@app.get("/")
def root():
    return {"message": "ACP Gateway running"}


# Create tables (temporary MVP). Later we will use Alembic.
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"ok": True, "service": "acp-gateway"}

@app.get("/health/db")
def health_db():
    ok = test_db_connection()
    return {"db": "ok" if ok else "fail"}
@app.get("/protected")
def protected(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    api_key = require_api_key(db, authorization)
    enforce_rpm(redis_client, api_key.id, api_key.rpm_limit)
    return {"ok": True, "tenant_id": api_key.tenant_id, "key_id": api_key.id}

