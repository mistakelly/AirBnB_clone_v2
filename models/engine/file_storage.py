#!/usr/bin/python3
"""
#!/Users/mistarkelly/vagrant_project/My-Projects/ALX-ONLY/AirBnB_clone_v2/.venv/bin/python3
    responsible for persisting object state in file_db.
"""
import json
from os import path
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import shlex


class FileStorage:
    """
        FileStorage.
    """
    ALL_CLASSES = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Place': Place,
        'Amenity': Amenity,
        'Review': Review
    }
    __file_path = 'file.json'
    __objects = {}

    def new(self, obj) -> None:

        """
            this adding New Object to file storage.
        """
        # construct key
        key = "{}.{}".format(
            obj.__class__.__name__, obj.id
        )
        self.__objects[key] = obj

    # echo 'all State' | HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd
    # HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db ./console.py
    def all(self, cls=None) -> dict:
        """
            this method is responsible for returning the whole
            object in the file __objects dictionary.
        """
        all_objects = {}
        if cls:
            for k, v in self.__objects.items():
                cls_name, cls_id = k.split('.')
                if cls.__name__ == cls_name:
                    all_objects[k] = v
            return all_objects
        for v in self.__objects.values():
            if hasattr(v, '_sa_instance_state'):
                delattr(v, '_sa_instance_state')
        return self.__objects

    def save(self) -> None:
        """
            for converting the python objects into python dictionary,
            so they can be stored into the file storage,this process is called
            serialization.
        """
        # declare dictionary.
        serialized_obj = {}

        for k, v in self.__objects.items():
            # call the to_dict method in the basemodel
            # to represent every object to dict.
            serialized_obj[k] = v.to_dict()
        # dump into file storage
        with open(self.__file_path, "w") as obj_dic:
            json.dump(serialized_obj, obj_dic)

    def reload(self) -> None:
        """
            responsible for reloading the object in file storage and
            dynamically create objects out of the data in the file storage
        """

        # open file
        # split the key of the dictionary
        # dynamically create classes base on the class name.
        if path.exists(self.__file_path) and\
                path.getsize(self.__file_path) > 0:
            with open(self.__file_path, "r") as db:
                try:
                    file_content = json.load(db)

                    for k, v in file_content.items():

                        # split the dictionary key
                        cls_name, cls_key = k.split('.')

                        # dynamically create the class object
                        # again according to the entry in db.

                        # same as doing.
                        global_class = self.ALL_CLASSES[cls_name]

                        result = global_class(**v)
                        # print(result)

                        self.__objects[k] = result
                except json.decoder.JSONDecodeError:
                    print('Unable to serialize')
                    exit(0)

    def delete(self, obj=None):
        """
            responsible deleting of objects
        """
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            del self.__objects[key]
