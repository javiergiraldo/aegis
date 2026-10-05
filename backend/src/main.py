import time

from fastapi import Depends, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.infrastructure.database.session import get_db
from src.infrastructure.websockets.server import get_socketio_app

# Definición de Métricas de Prometheus
REQUEST_COUNT = Counter('aegis_http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('aegis_http_request_duration_seconds', 'HTTP request latency', ['endpoint'])

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

    @app.middleware("http")
    async def add_prometheus_metrics(request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Filtramos las peticiones del socket.io para no inflar las métricas REST
        if not str(request.url.path).startswith("/socket.io"):
            REQUEST_LATENCY.labels(endpoint=request.url.path).observe(process_time)
            REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, http_status=response.status_code).inc()
        return response

    @app.get("/api/health")
    async def health_check(db: Session = Depends(get_db)):
        try:
            # Observabilidad: Verifica la conexión real con el motor de base de datos
            db.execute(text("SELECT 1"))
            db_status = "connected"
        except Exception:
            db_status = "disconnected"
            
        return {
            "status": "ok",
            "service": "Aegis Core Controller",
            "environment": "production",
            "database": db_status
        }
        
    @app.get("/metrics")
    async def metrics():
        """Endpoint para que el scraper de Prometheus lea la telemetría en texto plano."""
        return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

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
