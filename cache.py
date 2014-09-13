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
    uptime = IntegerField()
    cpu_temperature = FloatField()
    gpu_temperature = FloatField()
    memory_total = IntegerField()
    memory_used = IntegerField()
    hdd_total = IntegerField()
    hdd_used = IntegerField()
    at = DateTimeField()
