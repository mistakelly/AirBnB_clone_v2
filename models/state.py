#!/usr/bin/python3
"""
State class for creating State table
#!/Users/mistarkelly/vagrant_project/My-Projects/ALX-ONLY/AirBnB_clone_v2/.venv/bin/python3

"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from models.city import City
import models
import shlex


class State(BaseModel, Base):
    """
         state table.
         would be a Table in the database.
     """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        var = models.storage.all()
        lista = []
        result = []
        for key in var:
            city = key.replace('.', ' ')
            city = shlex.split(city)
            if city[0] == 'City':
                lista.append(var[key])
        for elem in lista:
            if elem.state_id == self.id:
                result.append(elem)
        return result
