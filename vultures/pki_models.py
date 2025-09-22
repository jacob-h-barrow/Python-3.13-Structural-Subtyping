from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine("sqlite:///pki.db", echo=False)
Base = declarative_base()

# Link to user in authentication_db or CRL. must sure present/not
# Split to run multiple cursors over this/keep separate
class PublicKey(Base):
    __tablename__ = "public_keys"
    
    id = Column(Integer, primary_key=True)
    
    uuid = Column(String, unique=True)
    ## Public_Key stored at n and e
    ## Verify key is not getting truncated
    public_key_n = Column(Integer)
    public_key_e = Column(Integer)
    
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    
Base.metadata.create_all(engine)
