from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import getenv

from utils.settings import ENV_PATH

load_dotenv(ENV_PATH)

# Database sozlamalari
engine = create_engine(getenv('DATABASE_URL'), echo=False)

Base = declarative_base()


# Database modellari
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, nullable=True)
    full_name = Column(String)
    conversion_count = Column(Integer, default=0)
    is_blocked = Column(Boolean, default=False)
    invited_by = Column(BigInteger, nullable=True)
    invited_count = Column(Integer, default=0)
    registration_date = Column(DateTime, default=datetime.now)
    last_conversion = Column(DateTime, nullable=True)


# Database yaratish
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)
