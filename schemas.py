from pydantic import BaseModel 
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models import Coupon

class CouponCreate(BaseModel):
   coupon_type: str
   partner_name : str
   validity_month: int
   
class CouponUpdate(BaseModel):
   code : str
   
class CouponOut(BaseModel):
    coupon_code : str
    coupon_type: str
    partner_name : str
    valid_until: str
       
class CreateResponse(JSONResponse):
    
    def __init__(self, message) -> None:
        super().__init__(content={"coupon_code":message}, status_code = 201)
        
class UpdateResponse(JSONResponse):
    
    def __init__(self) -> None:
        super().__init__(content={}, status_code = 204)
    
class ValidityResponse(JSONResponse):
    
    def __init__(self, message: str, coupon: CouponOut | None = None) -> None:
        super().__init__(
            content={
                "validity":message,
                "coupon_info" : {} if coupon is None else jsonable_encoder(coupon.model_dump()) 
            }, status_code=200)
        