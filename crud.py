from sqlalchemy.orm import Session
from models import CouponType, Partner, Coupon

def create_coupon(db: Session, coupon: Coupon) -> Coupon:
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon


def create_partner(db: Session, partner: Partner) -> Partner:
    db.add(partner)
    db.commit()
    db.refresh(partner)
    return partner

def retrieve_partner_by_name(db: Session, name: str) -> Partner:
    return db.query(Partner).filter_by(name = name).first()

def retrieve_coupontype_by_name(db: Session, name: str) -> Session:
    return db.query(CouponType).filter_by(name = name).first()

def retrieve_coupon(db: Session, id: int) -> Coupon: 
    return db.query(Coupon).filter_by(id = id).one_or_none()

def update_coupon_used_field(db: Session, coupon: Coupon) -> None: 

    setattr(coupon, 'used',  True)    
    db.add(coupon)
    db.commit()
    db.refresh(coupon)

