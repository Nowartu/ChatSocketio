from sqlalchemy import create_engine, Column, Text, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

engine = create_engine(
    "sqlite:///./test.db", connect_args={"check_same_thread": False}
)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_session_fa():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

users = [
    {
        "login": "admin",
        "password": "admin",
        "token": ''#"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJleHAiOjE3Mzg2MjIxMTd9.MjTspK8k5WiVDhxj7I4v9Bw2j3nRKGqratQHf8IFYLU"
    }
]

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    send_time = Column(DateTime)
    sender = Column(String(50), nullable=False)
    message = Column(Text)

Base.metadata.create_all(bind=engine)