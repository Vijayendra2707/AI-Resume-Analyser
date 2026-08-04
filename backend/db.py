import datetime
import os
from sqlalchemy import Float, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(String(50), default="candidate") # "admin" or "candidate"
    
    # Relationship: One user can have many records
    records = relationship("AnalysisRecord", back_populates="owner")
class AnalysisRecord(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    candidate_name = Column(String(255))
    score = Column(Float)
    shortlisted = Column(Integer)
    confidence = Column(Float)
    matched_skills = Column(JSON) 
    missing_skills = Column(JSON)
    report_url = Column(String(500)) # 🔴 ADD THIS LINE
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="records")
    
# This creates the table if it doesn't exist
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()