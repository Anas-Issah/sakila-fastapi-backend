from fastapi.exceptions import RequestValidationError

import repositories.customer_repository as customer_repo
from exceptions.customer import CustomerNotFound,CustomersNotFound,CustomerSearchError

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

def search_customers(first_name:str | None,last_name:str | None,conn):

    if first_name is None and last_name is None:
        raise CustomerSearchError
    
    if first_name:
        first_name = first_name.title()

    if last_name:
        last_name = last_name.title()

    customers = customer_repo.search_customer(first_name,last_name,conn)

    if not customers:
        raise CustomerNotFound
    
    if len(customers) > 1:
        
        return [
             {
        "customer_id": customer[0],
        "customer_first_name": customer[1],
        "customer_last_name": customer[2],
        "customer_email": customer[3]
    }
    for customer in customers
    ]

    else:
        return {
        
        "customer_id":customers[0][0],
        "customer_first_name":customers[0][1],
        "customer_last_name":customers[0][2],
        "customer_email":customers[0][3]
    
    }



def get_customers(page:int | None,limit: int | None,conn):

    if page != None:
        if page < 0:
            raise ValueError
    
        if limit is None:
            limit = 10

        offset = (page -1) * limit
    
    
    else:
        offset = page

    if limit and limit < 0:
            raise ValueError
    
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