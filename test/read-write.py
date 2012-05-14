import db
from models import *

db.sql.init()
db.destroyTables()
db.createTables()
db.commit()

print "====== WRITING DATA ======"

a1 = A()
a1.title = "A 1"
a1.save()

a2 = A()
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

db.commit()
the_a1_id = a1.id

db.clearCache()

print "====== READING DATA ======"

print A.get(the_a1_id).title, "== A 1"
print A.select("WHERE title = :title", title = "Test 2")[0].title, "== Test 2"
print A.select("WHERE title = 'Test 2'")[0].title, "== Test 2"
print len(A.select("WHERE title LIKE 'test%' ORDER BY title DESC")), "== 2"
