from sqlalchemy import Column, VARCHAR, Integer

from db.models import BaseModel


class DBMessage(BaseModel):

    __tablename__ = 'messages'

    sender_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    message = Column(VARCHAR(5000), nullable=False)
