from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from schemas import CouponCreate, CouponUpdate
from models import Coupon, Partner
from utils import valid_partner, valid_coupon, get_db, calc_date, generate_code
from schemas import CreateResponse, UpdateResponse, ValidityResponse, CouponOut
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import crud

router = APIRouter()

@router.post("/create")
async def create_coupon_service(request: CouponCreate, db: Session = Depends(get_db)) -> JSONResponse:
    
    """Creates a new coupon if the coupon information is valid

    Returns:
        JSONResponse: in case of valid request returns an empty json with status code 204
    """
    
    coupon_type = crud.retrieve_coupontype_by_name(db, request.coupon_type)
    if coupon_type is None:
        raise HTTPException(400, detail="Invalid coupon type")
    
    partner = crud.retrieve_partner_by_name(db, request.partner_name)
    if partner is None:
        if valid_partner(request.partner_name):
            partner = crud.create_partner(db, Partner(name = request.partner_name)) 
        else:
            raise HTTPException(400, detail="Invalid partner")

    coupon = crud.create_coupon(
        db=db, 
        coupon=Coupon(
            id = generate_code(),
            type_id = coupon_type.id, 
            partner_id = partner.id, 
            used = False, 
            valid_until = calc_date(request)
        )
    )      
          
    return CreateResponse(coupon.id)


@router.get("/validity")
async def get_coupon(code: str, db: Session = Depends(get_db)) -> JSONResponse:
    
    """Checks the validity of a coupon

    Returns:
        JSONResponse: in case of valid coupon returns 1 with the corresponding information otherwise 0
    """
    
    coupon = crud.retrieve_coupon(db, code)
    
    if coupon is None:
        raise HTTPException(400, detail="Invalid coupon id")
    
    if valid_coupon(coupon):
        return ValidityResponse(1, CouponOut(
            coupon_code = coupon.id,
            coupon_type = crud.retrieve_coupontype_by_id(db, coupon.type_id).name,
            partner_name = crud.retrieve_partner_by_id(db, coupon.partner_id).name,
            valid_until=coupon.valid_until.strftime("%x")      
        ))
    
    return ValidityResponse(0)

@router.post("/use")
async def use_coupon(request: CouponUpdate, db: Session = Depends(get_db)):
    
    """Deactivates a coupon if it is possible

    Returns:
        UpdateResponse: if the coupon has been deactivated successfully returns with status code 201
    """
    
    coupon = crud.retrieve_coupon(db, request.code)
    
    if coupon is None:
        raise HTTPException(400, detail="Invalid coupon code")
    
    if not valid_coupon(coupon):
        raise HTTPException(400, detail="This coupon has already been used or has expired")
        
    crud.update_coupon_used_field(db, coupon)
    
    return UpdateResponse()
    

        