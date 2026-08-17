from app.database import SessionLocal
from app.models.user import User
from app.auth import hash_password

db = SessionLocal()

existing = db.query(User).filter(User.email == "adarshsahay019@gmail.com").first()
if existing:
    existing.password_hash = hash_password("guukhaale")
    print("Updated existing user's password.")
else:
    new_user = User(email="adarshsahay019@gmail.com", password_hash=hash_password("CHOOSE-A-REAL-PASSWORD-HERE"))
    db.add(new_user)
    print("Created new user.")

db.commit()
db.close()