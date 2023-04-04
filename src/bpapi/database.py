from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///../bp.sqlite"
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
