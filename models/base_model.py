#!/usr/bin/python3
"""
#!/Users/mistarkelly/vagrant_project/My-Projects/ALX-ONLY/AirBnB_clone_v2/.venv/bin/python3
#!/usr/bin/python3
    BaseModel for creating every single attributes
    that will be inherited for all objects
"""

import uuid
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime
import models


Base = declarative_base()


class BaseModel:
    """
        this is for object creation.
    """

    TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, **kwargs):
        """
            init function
        """
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    value = datetime.strptime(value, self.TIME_FORMAT)
                if key != '__class__':
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
        else:
            import models
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self) -> str:
        """
            str function
        """
        obj_str = "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.__dict__
        )
        return obj_str

    def save(self):
        """
            save method
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self) -> dict:
        """
            dic method
        """
        if hasattr(self, '_sa_instance_state'):
            delattr(self, '_sa_instance_state')

        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__

        for k, v in obj_dict.items():
            if isinstance(v, datetime):
                obj_dict[k] = v.isoformat()

        return obj_dict

    def delete(self):
        """
            delete the current instance
        """
        models.storage.delete(self)
