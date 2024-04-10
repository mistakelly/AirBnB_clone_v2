#!/usr/bin/python3
"""
#!/Users/mistarkelly/vagrant_project/My-Projects/ALX-ONLY/AirBnB_clone_v2/.venv/bin/python3
This module instantiates an object of class DBStorage
if the environment variable HBNB_TYPE_STORAGE is equal to db,
otherwise it instantiates an object of class FileStorage
"""
from os import getenv
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

if getenv('HBNB_TYPE_STORAGE') == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()
storage.reload()
