from fastapi import APIRouter
from dal import * 

router = APIRouter()

@router.get('/analytics/top-customers')
def get_top_customers():
    return {"res":top_customers()}

@router.get('/analytics/customers-without-orders')
def without_orders():
    return {'res':get_inactive_customers()}

@router.get('/analytics/zero-credit-active-customers')
def active():
    return {'res':get_zero_credit_active_customers()}