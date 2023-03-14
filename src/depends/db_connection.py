from db import SessionLocal
from sqlalchemy.orm import Session
from utils.throws import throws

@throws([

])
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = (
    'get_db',
    'Session'
)
