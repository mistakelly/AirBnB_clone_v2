#!/usr/bin/python3
"""
#!/Users/mistarkelly/vagrant_project/My-Projects/ALX-ONLY/AirBnB_clone_v2/.venv/bin/python3
new class for sqlAlchemy
"""
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from models.base_model import Base, BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        all_classes = {}
        model_classes = [State, City, User, Place, Review, Amenity]
        if cls:
            query = self.__session.query(cls)
            for v in query:
                key = "{}.{}".format(v.__class__.__name__, v.id)
                all_classes[key] = v
            return all_classes

        for cls in model_classes:
            queries = self.__session.query(cls).all()
            for query in queries:
                key = "{}.{}".format(query.__class__.__name__, query.id)
                all_classes[key] = query
        return all_classes

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        try:
            # Create metadata
            Base.metadata.create_all(self.__engine)
            # Create a new session
            self.__session = scoped_session(sessionmaker(
                bind=self.__engine, expire_on_commit=True))
        except Exception as e:
            # Handle any errors that occur during
            # metadata creation or session initialization
            print(f"Error occurred during reload: {e}")

    def close(self):
        self.__session.close()
