from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True,future=True)

SessionLocal = sessionmaker(bind = engine, autoflush = False,autocommit =
False, future = True )

Base = declarative_base()

# dependency
from typing import Generator

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


