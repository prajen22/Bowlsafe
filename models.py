from sqlalchemy import Column, Integer, String, Date
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)

    overs = Column(Integer, nullable=False)
    daily_target = Column(Integer, nullable=False)

    effort_level = Column(String, nullable=False)
    body_status = Column(String, nullable=False)
    session_type = Column(String, nullable=False)

    notes = Column(String, nullable=True)
