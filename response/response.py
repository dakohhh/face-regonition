
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import Request
from ast import literal_eval


def customResponse(status:int, msg:str="" , success=True, data=None,):

    return JSONResponse(
        status_code=status,
        content={
        "status":status,
        "msg": msg,
        "success": success,
        "data": data if data != None else None
        }
    )



class CustomResponse(JSONResponse):
    def __init__(self, msg, status=200, success=True, data=None) -> None:

        response = {
        "status":status,
        "msg": msg,
        "success": success,
        "data": data 
        }

        super().__init__(status_code=status, content=response)



