from fastapi import Request, status
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded



class UserExistExecption(Exception):
    def __init__(self, msg: str):
        self.msg = msg   

async def user_exist_exception_handler(request: Request, exception: UserExistExecption):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "status": status.HTTP_409_CONFLICT, 
            "msg": exception.msg,
            "success": False,
        },
    )

class UnauthorizedExecption(Exception):
    def __init__(self, msg: str):
        self.msg = msg   

async def unauthorized_exception_handler(request: Request, exception: UnauthorizedExecption):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "status": status.HTTP_401_UNAUTHORIZED,
            "msg": exception.msg,
            "success": False
        },
    )

class ServerErrorException(Exception):
    def __init__(self, msg: str):
        self.msg = msg   

async def server_exception_handler(request: Request, exception: ServerErrorException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "msg": exception.msg,
            "success": False
        },
    )



class NotFoundException(Exception):
    def __init__(self, msg:str):
        self.msg = msg

async def not_found(request: Request, exception: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "status": status.HTTP_404_NOT_FOUND,
            "msg": exception.msg,
            "success": False
        },
    )




class DatabaseException(Exception):
    def __init__(self, msg: str):
        self.msg = msg

        
async def not_found_exception_handler(request: Request, exception: DatabaseException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "msg": exception.msg,
            "success": False
        },
    )


class CredentialsException(Exception):
    def __init__(self, msg: str):
        self.msg = msg



async def credentail_exception_handler(request: Request, exception: CredentialsException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "status": status.HTTP_401_UNAUTHORIZED,
            "msg": exception.msg,
            "success": False
        },
        headers={"WWW-Authenticate": "Bearer"}
    )




class BadRequestException(Exception):
    def __init__(self, msg: str):
        self.msg = msg



async def bad_request_exception_handler(request: Request, exception: BadRequestException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": status.HTTP_400_BAD_REQUEST,
            "msg": exception.msg,
            "success": False
        },
    )



