def getClassByName(classname):
    parts = classname.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)            
    return m

class FieldHelper(object):
    def __init__(self, field):
        self.field = field
class FieldSetter(FieldHelper):
    def __call__(self, obj, value):
        obj._values[self.field] = value
class FieldGetter(FieldHelper):
    def __call__(self, obj):
        if not self.field in obj._values: return None
        return obj._values[self.field]
class FieldDeleter(FieldHelper):
    def __call__(self, obj):
        del obj._values[self.field]

class RelationHelper(FieldHelper):
    def __init__(self, field, model):
        self.field = field
        self.model = model
class RelationSetter(RelationHelper):
    def __call__(self, obj, value):
        obj._values[self.field] = getattr(value, self.model._primary.name) # set primary key in field
class RelationGetter(RelationHelper):
    def __call__(self, obj):
        if not self.field in obj._values: return None
        return self.model.get(obj._values[self.field]) # return object with primary key

