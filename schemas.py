from pydantic import BaseModel 
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models import Coupon

class CouponCreate(BaseModel):
   coupon_type: str
   partner_name : str
   validity_month: int
   
class CouponUpdate(BaseModel):
   id : int
       
class CreateResponse(JSONResponse):
    
    def __init__(self) -> None:
        super().__init__(content={}, status_code = 204)
        
class UpdateResponse(JSONResponse):
    
    def __init__(self) -> None:
        super().__init__(content={}, status_code = 204)
    
class ValidityResponse(JSONResponse):
    
    def __init__(self, message: str, coupon: Coupon | None = None) -> None:
        super().__init__(
            content={
                "validity":message,
                "coupon_info" : {} if coupon is None else jsonable_encoder(coupon) 
            }, status_code=200)
        