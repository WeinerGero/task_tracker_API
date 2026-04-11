"""

"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.endpoints import tasks
from app.services.exceptions import ServiceError


app = FastAPI(title="API трекера задач")

app.include_router(tasks.router, prefix="/api/v1")

@app.exception_handler(ServiceError)
async def service_exception_handler(request: Request, exc: ServiceError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )
