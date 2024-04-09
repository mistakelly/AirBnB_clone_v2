#!/usr/bin/python3
"""State class for creating State table"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from models.city import City


class State(BaseModel, Base):
    """
        state table.
        would be a Table in the database.
    """
    # __tablename__ = "states"
    # name = Column(String(128), nullable=False)
    # cities = relationship("City", cascade='all, delete, delete-orphan',
    #                       backref="state")

    name = ""
