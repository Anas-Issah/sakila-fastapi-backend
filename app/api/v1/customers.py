from typing import Annotated
from fastapi import APIRouter,Depends,Query

from database import get_db
import services.customer_services as customer_services
from schemas import CustomerResponse,CustomerSearch,NewCustomer




router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
    )

@router.get("/{customer_id}",
            response_model=CustomerResponse)
async def get_customer(customer_id:int, conn= Depends(get_db)):

    return customer_services.get_customer(customer_id,conn)

    
@router.get("/",response_model=list[CustomerResponse])
async def get_customers(offset:int | None = None,
                        limit:int | None = None,
                        conn=Depends(get_db)):

    return customer_services.get_customers(offset,limit,conn)


@router.get("/search/",
            response_model= CustomerResponse | list[CustomerResponse])
async def search_customer(customer:Annotated[CustomerSearch,Query()],
                    conn = Depends(get_db)):
 
    return customer_services.search_customers(customer.first_name,customer.last_name,conn)


@router.get("/{customer_id}/rentals")
async def get_customer_rental_history(customer_id:int,
                                      conn=Depends(get_db)):

    

        return customer_services.get_customer_rental_history(customer_id,conn)


@router.get("/{customer_id}/payment")
async def get_customer_payment_history(customer_id:int,
                                      conn=Depends(get_db)):

    

        return customer_services.get_customer_payment_history(customer_id,conn)  

@router.post("")
async def add_customer(customer:NewCustomer,conn=Depends(get_db)):

      return customer_services.add_customer(
            customer.store_id,customer.first_name,
            customer.last_name,customer.email,
            customer.address_id,
            conn
      )