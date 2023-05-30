from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import ApiSettings
settings = ApiSettings()


DATABASE_URL = f"sqlite:///{settings.DATABASE_PATH}"
engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False},
    echo=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
