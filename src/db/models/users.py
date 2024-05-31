import re
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import validates 
from db.engine import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)

    def __str__(self):
        return self.email
    
    @validates('email') 
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('No email provided')
        if not re.match("^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$", email):
            raise AssertionError('Provided email is not an email address') 
        return email