from sqlalchemy import Column, String, Integer
from db.engine import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)

    def __str__(self):
        return self.email
