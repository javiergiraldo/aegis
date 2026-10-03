from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.websockets.server import get_socketio_app

def create_app() -> FastAPI:
    """App Factory for Aegis Core API."""
    app = FastAPI(
        title="Aegis API",
        description="Core API for Aegis Security & Observability Platform",
        version="1.0.0"
    )

    # Allow CORS for development and frontend integrations
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict to frontend domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health")
    async def health_check():
        return {
            "status": "ok",
            "service": "Aegis Core Controller",
            "environment": "development"
        }

    # Integración de Adaptadores REST (Casos de Uso)
    from src.infrastructure.api.routers.alerts import router as alerts_router
    app.include_router(alerts_router, prefix="/api/v1/alerts", tags=["Alerts"])

    return app

# Initialize the FastAPI Application
fastapi_app = create_app()

# Integración del Worker asíncrono
import asyncio
from src.infrastructure.workers.cert_manager import CertManagerWorker

@fastapi_app.on_event("startup")
async def startup_event():
    # Inicializa el CertManager para que realice barridos cada 60 segundos (simulación)
    worker = CertManagerWorker(check_interval_seconds=60)
    asyncio.create_task(worker.start())

# Mount Socket.IO App into FastAPI to create a unified ASGI application
socket_app = get_socketio_app(fastapi_app)

# The application is executed via uvicorn:
# uvicorn src.main:socket_app --host 0.0.0.0 --port 8000 --reload
