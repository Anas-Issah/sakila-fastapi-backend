from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from psycopg.errors import Error as DatabaseError

from contextlib import asynccontextmanager
import logging

from api.v1.router import api_v1_router
from core.app_logging import logging_setup
from exceptions.customer import (CustomerNotFound,CustomersNotFound,
                                 CustomerSearchError,CustomerValueError,
                                 CustomerHistoryError,CustomerPaymentError,
                                 AddCustomerError,StoreIDError,AddressIDError,
                                 StoreExistError,AddressExistError)

from exceptions.film import FilmsNotFound,FilmNotFound,FilmTitleError
from exceptions.users import UsernamePasswordValueError,UsernameTaken

logging_setup()
logger = logging.getLogger(__name__)




@asynccontextmanager
async def lifespan(app:FastAPI):

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins="https://localhost:300",
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

app.include_router(api_v1_router)

    
@app.middleware("http")
async def log_request(request:Request,call_next):
    "middleware to log request response"

    response = await call_next(request)

    logger.info("HTTP request",
                extra={
                    "method":request.method,
                    "path":request.url.path,
                    "statuscode":response.status_code
                })
    return response




# exception handlers

# request validation error
@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(request:Request,exc:RequestValidationError):

    return JSONResponse(
        status_code=422,
        content={
            "error":"Request validation error",
            "details":exc.errors()
        }
    )


# customers
@app.exception_handler(CustomerNotFound)
async def customer_not_found_error_handler(request:Request,exc:CustomerNotFound):
    
    return JSONResponse(
            status_code=404,
            content={
                "error":"CustomerNotFound error",
                "details":"Customer do not exist"
            }
    )

@app.exception_handler(CustomersNotFound)
async def customers_not_found_error_handler(request:Request,exc:CustomersNotFound):
    
    return JSONResponse(
            status_code=404,
            content={
                "error":"CustomersNotFound error",
                "details":"Customers do not exist"
            }
    )

@app.exception_handler(CustomerSearchError)
async def customer_search_error_handler(request:Request,exc:CustomerSearchError):

    return JSONResponse(
        status_code=422,
        content={
            "error":"Customer search error",
            "details":"Both first name and last name can not be null"
        }
    )

@app.exception_handler(CustomerHistoryError)
async def customer_rental_history_Error_handler(request:Request,exc:CustomerHistoryError):

    return JSONResponse(
        status_code=404,
        content={
            "error":"Customer history error",
            "details":"Customer or customer rental history does not exist"
        }
    )


@app.exception_handler(CustomerValueError)
async def customer_value_error_handler(request:Request,exc:CustomerValueError):

    return JSONResponse(
        status_code=422,
        content={
            "error":"Customer value error",
            "detail":"Any of the fields can not be whitespace"
        }
    )

@app.exception_handler(CustomerPaymentError)
async def customer_payment_history_error_handler(request:Request,exc:CustomerPaymentError):

    return JSONResponse(
        status_code=404,
        content={
            "error":"Customer payment error",
            "detail":"Customer or customer payment history does not exist"
        }
    )

@app.exception_handler(AddCustomerError)
async def add_customer_error_handler(request:Request,exc:AddCustomerError):

    return JSONResponse(
        status_code=500,
        content={
            "error":"Add customer error",
            "detail":"Adding new customer unsuccessful"
        }
    )

@app.exception_handler(StoreIDError)
async def store_id_error_handler(request:Request,exc:StoreIDError):

    return JSONResponse(
        status_code=404,
        content={
            "error":"Store id error",
            "detail":"Store id provided does not exist"
        }
    )

@app.exception_handler(AddressIDError)
async def address_id_error_handler(request:Request,exc:AddressIDError):

    return JSONResponse(
        status_code=404,
        content={
            "error":"Address id error",
            "detail":"Address id provided does not exist"
        }
    )

@app.exception_handler(StoreExistError)
async def store_exist_error_handler(request:Request,exc:StoreExistError):

    return JSONResponse(
        status_code=404,
        content={
            "error":"Store exist error",
            "detail":"Store entity do not exist"
        }
    )

@app.exception_handler(StoreExistError)
async def address_exist_error_handler(request:Request,exc:StoreExistError):

    return JSONResponse(
        status_code=404,
        content={
            "error":"Address exist error",
            "detail":"Address entity do not exist"
        }
    )

# films
@app.exception_handler(FilmNotFound)
async def films_not_found_error_handler(request:Request,exc:FilmNotFound):

    return JSONResponse(
        status_code=404,
        content={
            "error":"FilmNotFound error",
            "details":"Film not found"
        }
    )

@app.exception_handler(FilmsNotFound)
async def film_not_found_error_handler(request:Request,exc:FilmsNotFound):

    return JSONResponse(
        status_code=404,
        content={
            "error":"FilmsNotFound error",
            "details":"Films does not exist"
        }
    )


@app.exception_handler(FilmTitleError)
async def film_title_error_handler(request:Request,exc:FilmTitleError):

    return JSONResponse(
        status_code=422,
        content={
            "error":"Film title error",
            "details":"Film title can not be empty"
        }
    )

# users

@app.exception_handler(UsernameTaken)
async def username_taken_error_handler(request:Request,exc:UsernameTaken):

    return JSONResponse(
        status_code=422,
        content={
            "error":"Username taken error",
            "details":"Username taken by another user"
        }
    )

@app.exception_handler(UsernamePasswordValueError)
async def username_password_value_error_handler(request:Request,exc:UsernamePasswordValueError):

    return JSONResponse(
        status_code=422,
        content={
            "error":"Username Password value error",
            "details":"username and password cannot be empty or a whitespace"
        }
    )


# psycopg
@app.exception_handler(DatabaseError)
async def psycopg_error_handler(request:Request,exc:DatabaseError):
    
    return JSONResponse(
            status_code=500,
            content={
                "error":"Database error",
                "details":"A database error occured"
            }
    )


# general

@app.exception_handler(ValueError)
async def value_error_handler(request:Request,exc:ValueError):

    return JSONResponse(
        status_code=422,
        content={
            "error":"Value error",
            "details":"Digit should not be negative",
        
        }
    )