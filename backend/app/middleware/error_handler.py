from fastapi import Request
from fastapi.responses import JSONResponse
from ..utils.logger import error_logger

async def error_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        error_logger.error(f"Error processing request: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": str(e)
            }
        ) 