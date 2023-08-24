from config import SessionLocal
from datetime import date
from models import Partner, Coupon
from schemas import CouponCreate
from datetime import date
from dateutil.relativedelta import relativedelta
import random
import string

CODE_LENGTH = 10

def generate_code() -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

def valid_partner(partner: Partner) -> bool: 
    return True

def valid_coupon(coupon: Coupon) -> bool: 
    return not coupon.used and coupon.valid_until >= date.today()

def calc_date(cc: CouponCreate) -> date:
    return date.today() + relativedelta(months=cc.validity_month)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()