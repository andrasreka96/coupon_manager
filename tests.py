#utils test
from utils import valid_coupon
from models import Coupon
import datetime

def test_expired_coupon_is_invalid():
    
    assert valid_coupon(Coupon(
        id = 1,
        partner_id = 1,
        type_id = 1,
        valid_until = datetime.date(2023, 5, 17),
        used = False
    )) == False
    
def test_used_coupon_is_invalid():
    
    assert valid_coupon(Coupon(
        id = 1,
        partner_id = 1,
        type_id = 1,
        valid_until = datetime.date(2024, 5, 17),
        used = True
    )) == False
    
#end point test
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Coupon Manager Server is up"}

def test_create_coupon_and_test_get_coupon():
    
    update_coupon = {
        "coupon_type": "discount",
        "partner_name": "PLACEHOLDER",
        "validity_month": 2,
    }
    
    response_1 = client.post("/cup/create/", json=update_coupon)
    assert response_1.status_code == 201
    
    created_coupon = dict(response_1.json())    
    response_2 = client.get("/cup/validity?code=" + created_coupon['coupon_code'])
    returned_coupon = dict(response_2.json())
    
    assert created_coupon['coupon_code'] == returned_coupon['coupon_info']['coupon_code']
    assert "PLACEHOLDER" == returned_coupon['coupon_info']['partner_name']
    assert returned_coupon['validity'] == 1
    
if __name__ == "__main__":
    
    test_expired_coupon_is_invalid()
    test_used_coupon_is_invalid()
    test_root()
    test_create_coupon_and_test_get_coupon()