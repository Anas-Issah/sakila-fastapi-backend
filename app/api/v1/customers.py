from fastapi import APIRouter,Depends,HTTPException,Query

from database import get_db
import services.customer_services as customer_services
from schemas import CustomerResponse,CustomerNotFound




router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
    )

@router.get("/{customer_id}",
            response_model=CustomerResponse)
async def get_customer(customer_id:int, conn= Depends(get_db)):

    return customer_services.get_customer(customer_id,conn)
    




@router.get("/",response_model=list[CustomerResponse])
async def get_customers(offset:int = Query(0,ge=0),
                        limit:int = Query(10,ge=1,le=10),
                        conn=Depends(get_db)):

    return customer_services.get_customers(offset,limit,conn)
  

