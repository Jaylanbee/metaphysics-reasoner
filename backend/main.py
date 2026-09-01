from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from backend.config import settings

from backend.logging_config import setup_logging
from backend.metrics import MetricsMiddleware, metrics_endpoint
from backend.health import router as health_router
from backend.routers import batch, statistics, report

setup_logging(settings.APP_ENV)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Eastern Metaphysics Reasoning Engine API",
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(MetricsMiddleware)

app.include_router(health_router, tags=["Health"])
app.include_router(batch.router, prefix="/api/v1/batch", tags=["Batch Processing"])
app.include_router(statistics.router, prefix="/api/v1/statistics", tags=["Statistics"])
app.include_router(report.router, prefix="/api/v1/report", tags=["Report Generator"])
app.add_route("/metrics", metrics_endpoint)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal Server Error", "detail": str(exc)},
    )
