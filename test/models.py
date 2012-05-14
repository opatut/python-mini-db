import db

@db.model
class A(db.Model):
    _fields = [
        db.Field("id", int, primary = True),
        db.Field("title", unicode)
        ]

@db.model
class B(db.Model):
    _fields = [
        db.Field("id", int, primary = True),
        db.Field("a", A)
        ]
