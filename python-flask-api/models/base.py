from peewee import *

from db.db import db

class BaseModel(Model):
    class Meta:
        database = db
