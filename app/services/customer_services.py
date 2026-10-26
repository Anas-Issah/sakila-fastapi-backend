from fastapi.exceptions import RequestValidationError

import repositories.customer_repository as customer_repo
from exceptions.customer import (CustomerNotFound,CustomersNotFound,CustomerSearchError,
                                 CustomerHistoryError,CustomerPaymentError,StoreIDError,
                                 AddressIDError,AddCustomerError,StoreExistError,
                                 AddressExistError)

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

def get_customer_rental_history(customer_id:int,conn):

    rental_history = customer_repo.get_customer_rental_history(customer_id,conn)

    if not rental_history:
        raise CustomerHistoryError


    return [
            {"customer_id":history[0],
             "customer_name":history[1],
             "rental_id":history[2],
             "film_title":history[3],
             "rental_date":history[4]}
             for history in rental_history
        ]

def get_customer_payment_history(customer_id:int,conn):

    payment_history = customer_repo.get_customer_payment_history(customer_id,conn)

    if not payment_history:
        raise CustomerPaymentError


    return [
            {"customer_id":history[0],
             "customer_name":history[1],
             "rental_id":history[2],
             "payment_id":history[3],
             "amount":history[4],
             "payment_date":history[5]}
             for history in payment_history
        ]

def add_customer(store_id,first_name,
        last_name,email,address_id,
        conn):
    
    store_ids = customer_repo.get_store_ids(conn)
    if not store_ids:
        raise StoreExistError

    store_ids = [id[0] for id in store_ids]
    if store_id not in store_ids:
        raise StoreIDError

    address_ids = customer_repo.get_address_ids(conn)
    if not address_ids:
        raise AddressExistError
    
    address_ids =[id[0] for id in address_ids]
    if address_id not in address_ids:
        raise AddressIDError
    
    new_customer = customer_repo.add_customer(store_id,first_name,
                                            last_name,email,address_id,
                                            conn)

    if not new_customer:
        raise AddCustomerError

    return {
            "customer_id":new_customer[0],
            "store_id":new_customer[1],
            "first_name":new_customer[2],
            "last_name":new_customer[3],
            "email":new_customer[4]
        }


def delete_customer(customer_id:int,conn):

    customer = customer_repo.get_customer(customer_id,conn)

    if not customer:
        raise CustomerNotFound

    
    customer_repo.delete_customer(customer_id,conn)

    return {
        "stutuse_code":200,
        "details":f"customer with ID {customer_id} successfully deleted."
    }
    