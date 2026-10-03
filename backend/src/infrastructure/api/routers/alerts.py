from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database.session import get_db
from src.application.schemas.alert import SecurityAlertCreate, SecurityAlertResponse
from src.application.use_cases.security_cases import RegisterSecurityAlertUseCase

router = APIRouter()

@router.post("/", response_model=SecurityAlertResponse, status_code=status.HTTP_201_CREATED)
async def create_security_alert(
    alert_in: SecurityAlertCreate, 
    db: Session = Depends(get_db)
):
    """
    Adaptador REST: Endpoint para ingestar una nueva alerta de seguridad.
    Ejecuta el caso de uso para persistir en BD y hacer el broadcast por WebSocket.
    """
    use_case = RegisterSecurityAlertUseCase(db)
    try:
        # Utilizamos await ya que el caso de uso despacha el evento WebSocket asíncronamente
        return await use_case.execute(alert_in)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
