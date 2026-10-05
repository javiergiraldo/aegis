import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuración agnóstica del entorno
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://aegis_admin:secure_password_demo_123@localhost:5432/aegis_db"
)

# Inicialización del Engine y Session Factory
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Generador para inyección de dependencias de la sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
