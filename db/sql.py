from sqlalchemy import create_engine
from sqlalchemy.sql import text

engine = None
connection = None
transaction = None

def init():
    global engine, connection, transaction
    engine = create_engine('sqlite:////tmp/test.db', echo = False)
    connection = engine.connect()
    transaction = connection.begin()

def commit():
    global transaction
    #transaction.commit()
    #transaction = connection.begin()

class Query(object):
    def __init__(self, query):
        self.query = query
        self.result = None

    def run(self, *args, **kwargs):
        self.result = connection.execute(self.query, *args, **kwargs)
        return self.result
