from db.cache import *
from db.field import *
from db.helpers import *
from db.sql import *

from sqlalchemy.exc import OperationalError

models = {} # name->class

def destroyTables():
    for model in models:
        models[model].destroyTable()

def createTables():
    for model in models:
        models[model].createTable()

class Model(object):
    _fields = []
    _table = ""
    _primary = None

    def __init__(self):
        self._values = {}

    @property
    def _allValues(self):
        v = self._values
        for field in self._fields:
            if not field.name in v:
                v[field.name] = None
        return v

    @classmethod
    def get(model, key):
        cache = modelcache[model.__name__]
        if cache.has(key):
            return cache.get(key)

        r = model.select("WHERE %s = :key LIMIT 1" % model._primary.name, key = key)
        return r[0] if r else None

    @classmethod
    def select(model, options = "", *args, **kwargs):
        cache = modelcache[model.__name__]
        sql = "SELECT * FROM %s" % model._table
        if options:
            sql += " " + options
        result = Query(sql).run(*args, **kwargs)
        models = []
        for row in result:
            m = model()
            for k, v in row.items():
                m._values[k] = v
            cache.set(m)
            models.append(m)
        return models


    def save(self):
        model = self.__class__
        cache = modelcache[model.__name__]
        cache.set(self)

        # save to SQL
        if len(model._fields) == 0 or len(self._values) == 0:
            raise Exception("A model needs at least 1 field set.")

        sql = "INSERT INTO %s (" % model._table
        for field in model._fields:
            if field.name in self._values:
                sql += field.name + ", "
        sql = sql[:-2] + ") VALUES ("
        for field in model._fields:
            if field.name in self._values:
                sql += ":" + field.name + ", "
        sql = sql[:-2] + ")"

        result = Query(sql).run(**self._values)

        if not self._primary.name in self._values:
            self._values[self._primary.name] = result.lastrowid

    @classmethod
    def createTable(model):
        sql = "CREATE TABLE %s (" % model._table
        for field in model._fields:
            sql += field.name + " " + field.sqlType + ", "
        sql = sql[:-2]
        #sql += "PRIMARY KEY %s" % model._primary.name
        sql += ");"

        Query(sql).run()

    @classmethod
    def destroyTable(model):
        sql = "DROP TABLE %s" % model._table
        try: Query(sql).run()
        except OperationalError: pass # table not found


def registerModel(cls):
    name = cls.__name__

    if name in models:
        if cls != models[name]:
            raise Exception("A Model named '%s' is already registered." % name)
        else:
            return # it's ok, we just re-registered the same model

    if not cls._table:
        cls._table = name.lower()

    table = cls._table

    models[name] = cls
    modelcache[name] = Cache(cls)

    new_fields = []
    for field in cls._fields:
        if issubclass(field.type, Model):
            registerModel(field.type)

            key = field.name + "_" + field.type._primary.name
            new_fields.append(Field(key, field.type._primary.type, primary = field.primary))

            def setter(self, value):
                self._values[key] = getattr(value, pri.name) # set primary key in field
            def getter(self):
                return ft.get(self._values[key]) # return object with primary key
            def deleter(self):
                del self._values[key]
            setattr(cls, field.name, property(RelationGetter(key, field.type), RelationSetter(key, field.type), FieldDeleter(key)))
        else:
            new_fields.append(field)

    cls._fields = new_fields

    for field in cls._fields:
        setattr(cls, field.name, property(FieldGetter(field.name), FieldSetter(field.name), FieldDeleter(field.name)))
        if field.primary:
            if cls._primary:
                raise Exception("Model %s already has %s as primary key." % (name, cls._primary.name))
            cls._primary = field

    if not cls._primary:
        raise Exception("Model %s does not have a primary field. A primary field is required for caching and accessing the data." % name)

# this is the decorator
def model(cls):
    registerModel(cls)
    return cls

