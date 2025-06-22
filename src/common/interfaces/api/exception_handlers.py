from fastapi import Request, status
from fastapi.responses import JSONResponse


async def any_exc_handler(req: Request, exc: Exception):
    return JSONResponse(
        content={"msg": "something wrong"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
