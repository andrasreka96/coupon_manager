from sqlalchemy import  Column, Integer, Date, ForeignKey, String, Boolean
from config import Base


class Partner(Base):
    
    __tablename__ ="partner"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), comment= 'Name of the partner company or person')
    
class CouponType(Base):
    
    __tablename__="coupon_type"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), comment= 'Type name')

class Coupon(Base):
    
    __tablename__ ="coupon"

    id = Column(Integer, primary_key=True, index=True)
    partner_id = Column(Integer, ForeignKey("partner.id"), comment = "coupon's partner id")
    type_id = Column(Integer, ForeignKey("coupon_type.id"), comment = "coupon's type id")
    valid_until = Column(Date)
    used = Column(Boolean)