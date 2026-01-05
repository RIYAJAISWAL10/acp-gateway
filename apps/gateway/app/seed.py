from app.db import SessionLocal, engine
from app.models import Base, Tenant, ApiKey
from app.auth import hash_key

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# create tenant
t = Tenant(name="demo")
db.add(t)
db.commit()
db.refresh(t)

# create api key
raw_key = "demo-secret-key"
k = ApiKey(tenant_id=t.id, key_hash=hash_key(raw_key), label="demo", rpm_limit=120)
db.add(k)
db.commit()

print("RAW API KEY:", raw_key)
