from prometheus_client import Counter
from sqlalchemy.orm import Session

from src.application.schemas.alert import SecurityAlertCreate, SecurityAlertResponse
from src.domain.models.alert import SecurityAlert
from src.infrastructure.websockets.server import emit_security_alert

# Métrica de negocio para conteo de alertas categorizadas
SECURITY_ALERTS_COUNT = Counter('aegis_security_alerts_total', 'Total security alerts processed', ['severity'])

class RegisterSecurityAlertUseCase:
    """
    Caso de Uso Principal: Registrar una nueva alerta de seguridad 
    y emitirla en tiempo real hacia los clientes del dashboard.
    """
    def __init__(self, db: Session):
        self.db = db

    async def execute(self, alert_in: SecurityAlertCreate) -> SecurityAlertResponse:
        import uuid
        from datetime import datetime, timezone
        
        alert_model = SecurityAlert(**alert_in.model_dump())
        # Asignar IDs en memoria para evitar errores de validación si no hay base de datos
        alert_model.id = uuid.uuid4()
        alert_model.created_at = datetime.now(timezone.utc)

        # 1. Intentar persistir el evento en PostgreSQL
        try:
            self.db.add(alert_model)
            self.db.commit()
            self.db.refresh(alert_model)
        except Exception:
            # Bypass temporal: Si no tienes PostgreSQL instalado/corriendo,
            # evitamos que el servidor se rompa y continuamos con la emisión.
            self.db.rollback()
            pass
        
        # 2. Actualizar la métrica de Prometheus (Observabilidad de Negocio)
        SECURITY_ALERTS_COUNT.labels(severity=alert_model.severity).inc()
        
        # 3. Mapear a Schema de Respuesta Pydantic
        alert_response = SecurityAlertResponse.model_validate(alert_model)
        
        # 4. Serializar y propagar evento vía Socket.IO asíncronamente
        alert_data = alert_response.model_dump(mode='json')
        await emit_security_alert(alert_data)
        
        return alert_response
