from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request

class ExceptionCustom(HTTPException):
    pass

async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"Error: {exc.detail}"}
    )