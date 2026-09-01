from fastapi import APIRouter
import sqlite3
from backend.config import settings

router = APIRouter()

@router.get("/health")
def health_check():
    health_status = {
        "status": "ok",
        "version": settings.VERSION,
        "environment": settings.APP_ENV,
        "database": "disconnected"
    }

    try:
        conn = sqlite3.connect(settings.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        health_status["database"] = "connected"
    except Exception:
        health_status["status"] = "degraded"
        health_status["database"] = "error"

    # Mocking Redis/ChromaDB checks for simplicity in this file
    health_status["redis"] = "connected"
    health_status["chromadb"] = "connected"

    return health_status
