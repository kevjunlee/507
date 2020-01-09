
import sqlite3

conn = sqlite3.connect('Northwind_small.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Employee')
for row in cur:
    print(row)


cur.execute('SELECT Id FROM "Order" WHERE OrderDate >= "2014-01-01"')
for row in cur:
    print(row)

cur.execute('SELECT CompanyName FROM "Customer" WHERE Region == "Northern Europe" OR Region == "Southern Europe" OR Region == "Western Europe" OR Region == "British Isles"')
for row in cur:
    print(row)
    
conn.close()
