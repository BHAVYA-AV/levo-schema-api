from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class SchemaVersion(Base):
    __tablename__ = "schema_versions"

    id = Column(Integer, primary_key=True, index=True)
    application = Column(String, index=True)
    service = Column(String, index=True)
    version = Column(Integer)
    filepath = Column(String)
    uploaded_at = Column(DateTime, default=func.now())
