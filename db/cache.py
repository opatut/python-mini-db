
modelcache = {} # name->cache

class Cache(object):
    """Stores instances of models by their primary key."""
    def __init__(self, modelclass):
        self.modelclass = modelclass
        self.data = {}

    def get(self, key):
        if not key in self.data: return None
        return self.data[key]

    def has(self, key):
        return key in self.data

    def set(self, value):
        if hasattr(value, self.modelclass._primary.name):
            key = getattr(value, self.modelclass._primary.name) # get the value of the primary key
            self.data[key] = value
