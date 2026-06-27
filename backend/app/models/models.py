
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from backend.app.database import Base

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    plan = Column(String, default="free")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer)
    sku = Column(String)
    title = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    status = Column(String)
    item_id = Column(String)
    error = Column(Text)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer)
    product_id = Column(Integer)
    status = Column(String)
    stage = Column(String)
    priority = Column(Integer, default=3)

class EventLog(Base):
    __tablename__ = "event_logs"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer)
    event = Column(String)
    payload = Column(Text)
