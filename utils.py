from config import SessionLocal
from datetime import date
from models import Partner, Coupon

def valid_partner(partner: Partner) -> bool: 
    return True

def valid_coupon(coupon: Coupon) -> bool: 
    return not coupon.used and coupon.valid_until >= date.today()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()