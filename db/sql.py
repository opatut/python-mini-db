from sqlalchemy.sql import text
from sqlalchemy import create_engine

engine = None
connection = None

def init():
    global engine, connection
    engine = create_engine('sqlite:///test.db', echo = True)
    connection = engine.connect()
    print "Connected."


class Query(object):
    def __init__(self, query):
        self.query = query
        self.result = None

    def run(self, **kwargs):
        self.result = connection.execute(self.query, kwargs)
        return self.result
