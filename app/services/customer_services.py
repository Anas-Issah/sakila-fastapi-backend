from fastapi import HTTPException

import repositories.customer_repository as customer_repo
from exceptions.customer import CustomerNotFound,CustomersNotFound

def get_customer(customer_id:int,conn):

    customer = customer_repo.get_customer(customer_id,conn)

    if not customer:
        raise CustomerNotFound

    return {
        
        "customer_id":customer[0],
        "customer_first_name":customer[1],
        "customer_last_name":customer[2],
        "customer_email":customer[3]
    
    }


def get_customers(offset:int | None,limit: int | None,conn):

    customers = customer_repo.get_customers(offset,limit,conn)



    if not customers:
        raise CustomersNotFound

    return [
             {
        "customer_id": customer[0],
        "customer_first_name": customer[1],
        "customer_last_name": customer[2],
        "customer_email": customer[3]
    }
    for customer in customers
    ]