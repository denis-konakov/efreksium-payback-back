from db import SessionLocal
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
__all__ = (
    'SessionLocal',
    'get_db'
)
