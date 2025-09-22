from sqlalchemy import Column, String, Integer, DateTime, LargeBinary, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine("sqlite:///authentication.db", echo=False)
Base = declarative_base()

# Link to authentication db; split for multiple cursors
class Session(Base):
    __tablename__ = "uuid"
    
    id = Column(Integer, primary_key=True)
    
    uuid = Column(String, unique=True)
    
    ip_address_used = Column(String)
    mac_used = Column(String)
    application_used = Column(String)
    
    onboard = Column(DateTime, default=datetime.now())

# Only sent tokens
class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    
    uuid = Column(String, ForeignKey('sessions.uuid')
    
    # Link to pki database's public_key 
    senders_public_key = Column(String)
    sent_token = Column(LargeBinary)
    signature = Column(LargeBinary)
    accepted = Column(Boolean)
    
    timestamp = Column(DateTime, default=datetime.now())
    
Base.metadata.create_all(engine)
