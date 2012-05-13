import db

db.sql.init()

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

a = A.get(100)
a = A.select("WHERE title LIKE '%1'")
A.get("WHERE id = :id ORDER_BY lol", id = 10000)
print a._values
