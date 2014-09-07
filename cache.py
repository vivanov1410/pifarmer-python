from peewee import *


class Cache:
    def __init__(self, name):
        self.name = name
        self._db = SqliteDatabase(name + '.db')