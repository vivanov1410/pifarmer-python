from peewee import *

db = SqliteDatabase('cache.db')


class Cache:
    def __init__(self):
        db.create_table(StatisticsReading, safe=True)


class BaseModel(Model):
    class Meta:
        database = db


class StatisticsReading(BaseModel):
    device_id = CharField()
    at = DateTimeField()
    cpu_temperature = FloatField()
    gpu_temperature = FloatField()
    # add other fields