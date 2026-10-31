from typing import Annotated
from fastapi import APIRouter,Depends,Query
from fastapi.security import OAuth2PasswordBearer

from database import get_db
import services.customer_services as customer_services
from schemas import CustomerResponse,CustomerSearch,NewCustomer
from services.user_services import get_current_user,user_rate_limit



router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
    )


@router.get("/{customer_id}",response_model=CustomerResponse,
            dependencies=[Depends(user_rate_limit(10,60))])
async def get_customer(customer_id:int, conn= Depends(get_db),
                       current_user=Depends(get_current_user)
                       ):

    return customer_services.get_customer(customer_id,conn)

    
@router.get("/",response_model=list[CustomerResponse],
            dependencies=[Depends(user_rate_limit(10,60))])
async def get_customers(offset:int | None = None,
                        limit:int | None = None,
                        conn=Depends(get_db),
                        current_user=Depends(get_current_user)
                    ):

    return customer_services.get_customers(offset,limit,conn)


@router.get("/search/",
            response_model= CustomerResponse | list[CustomerResponse],
            dependencies=[Depends(user_rate_limit(10,60))])
async def search_customer(customer:Annotated[CustomerSearch,Query()],
                    conn = Depends(get_db),
                    current_user=Depends(get_current_user)
                    ):
 
    return customer_services.search_customers(customer.first_name,customer.last_name,conn)


@router.get("/{customer_id}/rentals",dependencies=[Depends(user_rate_limit(10,60))])
async def get_customer_rental_history(customer_id:int,
                                      conn=Depends(get_db),
                                      current_user=Depends(get_current_user)):

        return customer_services.get_customer_rental_history(customer_id,conn)


@router.get("/{customer_id}/payment",dependencies=[Depends(user_rate_limit(10,60))])
async def get_customer_payment_history(customer_id:int,
                                    conn=Depends(get_db),
                                    current_user=Depends(get_current_user)

                                      ):

        return customer_services.get_customer_payment_history(customer_id,conn)  

@router.post("",dependencies=[Depends(user_rate_limit(10,60))])
async def add_customer(customer:NewCustomer,conn=Depends(get_db),
                    current_user=Depends(get_current_user)
                    ):

      return customer_services.add_customer(
            customer.store_id,customer.first_name,
            customer.last_name,customer.email,
            customer.address_id,
            conn
      )

@router.delete("/{customer_id}")
async def delete_customer(customer_id:int,conn=Depends(get_db),
                          current_user=Depends(get_current_user)):

    return customer_services.delete_customer(customer_id,conn)
