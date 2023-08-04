
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import Request
from ast import literal_eval





class CustomResponse(JSONResponse):
    def __init__(self, msg, status=200, success=True, data=None) -> None:

        response = {
        "status":status,
        "msg": msg,
        "success": success,
        "data": data 
        }

        super().__init__(status_code=status, content=response)



