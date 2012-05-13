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

A.createTable()
B.createTable()

a1 = A()
a1.title = "A 1"
a1.save()

a2 = A()
print a2._values
a2.title = "Test 2"
a2.save()

a11 = A()
a11.title = "Test 11"
a11.save()

b1 = B()
b1.id = 10
b1.a = a1
b1.save()
b2 = B.get(10)
