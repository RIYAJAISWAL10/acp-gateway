import hashlib
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import ApiKey

def hash_key(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def require_api_key(db: Session, authorization: str | None):
    # Expect: Authorization: Bearer <key>
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing API key")

    raw_key = authorization.split(" ", 1)[1].strip()
    key_hash = hash_key(raw_key)

    api_key = db.query(ApiKey).filter(ApiKey.key_hash == key_hash).first()
    if not api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return api_key
