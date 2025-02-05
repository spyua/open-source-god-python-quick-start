from sqlalchemy import Column, Integer, String
from app.database import Base

# user db models 
class User(Base):
    # 表格的名稱是 users
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
