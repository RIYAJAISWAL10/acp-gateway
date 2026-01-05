from app.db import SessionLocal
from app.models import ApiKey

db = SessionLocal()
k = db.query(ApiKey).first()
k.rpm_limit = 10
db.commit()
print("rpm_limit set to", k.rpm_limit)
