from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from psycopg.errors import Error as DatabaseError

from contextlib import asynccontextmanager
import logging

from api.v1.router import api_v1_router
from core.app_logging import logging_setup
from exceptions.customer import CustomerNotFound,CustomersNotFound


logging_setup()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app:FastAPI):

    yield

app = FastAPI(lifespan=lifespan)

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


# customer
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
