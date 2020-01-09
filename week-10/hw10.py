'''
SI 507 F18 homework 9: Basic SQL statements
'''

import sqlite3 as sqlite


conn = sqlite.connect('Northwind_small.sqlite')
cur = conn.cursor()

#----- Q1. Show all rows from the Region table 
print('-'*20 + "Question 1" + '-'*20)
def question1():
    region = []
    cur.execute('SELECT * FROM Region')
    for row in cur:
        print(row)
question1()
#----- Q2. How many customers are there? 
print('-'*20 + "Question 2" + '-'*20)
def question2():
    cur.execute('SELECT count(distinct Id) FROM Customer')
    for row in cur:
        print(row)

question2()
#----- Q3. How many orders have been made? 
print('-'*20 + "Question 3" + '-'*20)
def question3():
    cur.execute("SELECT count(Id) FROM 'Order'")
    for row in cur:
        print(row)
    
question3()

#----- Q4. Show the first five rows from the Product table 
print('-'*20 + "Question 4" + '-'*20)
def question4():
    cur.execute('SELECT * FROM Product')
    i = 0
    for row in cur:
        print(row)
        i += 1
        if i > 4:
            break
question4()

#----- Q5. Show the names of the five cheapest products 
print('-'*20 + "Question 5" + '-'*20)
def question5():
    cur.execute('SELECT * FROM Product ORDER BY UnitPrice asc')
    i = 0
    for row in cur:
        print(row)
        i += 1
        if i > 4:
            break

question5()
#----- Q6. Show the names and number of units in stock of all products that have more than 100 units in stock
print('-'*20 + "Question 6" + '-'*20)
def question6():
    cur.execute('SELECT ProductName, UnitsInStock FROM Product WHERE UnitsInStock > 100')
    for row in cur:
        print(row)

question6()

#----- Q7. Show all column names in the Order table 
print('-'*20 + "Question 7" + '-'*20)
def question7():
    cur.execute("PRAGMA table_info([order]);")
    for row in cur:
        print(row)
        
question7()

#----- Q8. Show the names of all customers who lives in USA and have a fax number on record.
print('-'*20 + "Question 8" + '-'*20)
def question8():
    cur.execute("SELECT ContactName FROM Customer WHERE Country == 'USA' AND Fax not null")
    for row in cur:
        print(row)
question8()

#----- Q9. Show the names of all the products, if any, that requires a reorder. 
# (If the units in stock of a product is lower than its reorder level but there's no units of the product currently on order, the product requires a reorder) 
print('-'*20 + "Question 9" + '-'*20)
def question9():
    cur.execute("SELECT ProductName FROM Product WHERE UnitsInStock < ReorderLevel AND UnitsOnOrder = 0")
    for row in cur:
        print(row)
question9()

#----- Q10. Show ids of all the orders that ship to France where postal code starts with "44"
print('-'*20 + "Question 10" + '-'*20)
def question10():
    cur.execute("SELECT Id FROM 'Order' WHERE ShipCountry = 'France' AND ShipPostalCode LIKE '44%'")
    for row in cur:
        print(row)

question10()
conn.close()
