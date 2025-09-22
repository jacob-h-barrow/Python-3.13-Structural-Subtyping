from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine("sqlite:///authentication.db", echo=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    
    uuid = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    
    onboard = Column(DateTime, default=datetime.now())

class Login(Base):
    __tablename__ = "logins"

    id = Column(Integer, primary_key=True)
    
    uuid = Column(String, ForeignKey('users.id'))
    timestamp = Column(DateTime, default=datetime.now())
    
Base.metadata.create_all(engine)
