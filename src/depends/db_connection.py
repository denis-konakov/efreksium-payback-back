from db import SessionLocal
from sqlalchemy.orm import Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
__all__ = (
    'get_db',
    'Session'
)
