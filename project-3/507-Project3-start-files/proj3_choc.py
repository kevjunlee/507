import sqlite3
import csv
import json
import pandas as pd

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from CSV and JSON into a new database called choc.db
DBNAME = 'choc.db'
BARSCSV = 'flavors_of_cacao_cleaned.csv'
COUNTRIESJSON = 'countries.json'

with open(COUNTRIESJSON) as file:
    json_country = json.load(file)
    
def make_bar_table():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = "DROP TABLE IF EXISTS 'Bars';"
    cur.execute(statement)
    
    statement = """
        CREATE TABLE 'Bars' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            'Company'   TEXT,
            'SpecificBeanBarName'   TEXT,
            'REF'   TEXT,
            'ReviewDate'    TEXT,
            'CocoaPercent'  REAL,
            'CompanyLocationId' INTEGER,
            'Rating'    REAL,
            'BeanType'  TEXT,
            'BroadBeanOriginId' INTEGER,
            
            FOREIGN KEY(CompanyLocationId) REFERENCES Countries(Id),
            FOREIGN KEY(BroadBeanOriginId) REFERENCES Countries(Id));
    """
    cur.execute(statement)
    conn.commit()
    conn.close()

make_bar_table()

def make_country_table():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = "DROP TABLE IF EXISTS 'Countries';"
    cur.execute(statement)
    
    statement = """
        CREATE TABLE 'Countries' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Alpha2' TEXT,
            'Alpha3' TEXT,
            'EnglishName' TEXT,
            'Region' TEXT,
            'Subregion' TEXT,
            'Population' INTEGER,
            'Area' REAL);
    """
    cur.execute(statement)
    conn.commit()
    conn.close()

make_country_table()

def populate_json():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    for x in json_country:
        insertion = (None, x["alpha2Code"], x ["alpha3Code"], x["name"], x["region"], x["subregion"], x["population"], x["area"])
        statement = "INSERT INTO 'Countries'"
        statement += "VALUES (?,?,?,?,?,?,?,?)"
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

populate_json()

def populate_csv():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    with open(BARSCSV, 'r', encoding='utf-8-sig') as f:
        bar_data = csv.reader(f)
        next(bar_data)
        for x in bar_data:
            insertion = [(x[0]),(x[1]),(x[2]),(x[3]),(float(x[4].strip('%'))),(x[5]),(x[6]),(x[7]),(x[8])]
            statement = "INSERT INTO Bars (Company, SpecificBeanBarName, REF, ReviewDate, CocoaPercent,\
            CompanyLocationId,Rating,BeanType,BroadBeanOriginId)"
            statement += "VALUES (?,?,?,?,?,?,?,?,?)"
            cur.execute(statement, insertion)
            conn.commit()
            
    statement2 = '''
        UPDATE Bars
        SET (CompanyLocationId) = (SELECT c.ID FROM Countries c WHERE Bars.CompanyLocationId = c.EnglishName)
    '''

    statement3 = '''
        UPDATE Bars
        SET (BroadBeanOriginId) = (SELECT c.ID FROM Countries c WHERE Bars.BroadBeanOriginId = c.EnglishName)
    '''
    cur.execute(statement2)
    cur.execute(statement3)
    conn.commit()
    conn.close()
populate_csv()


# Part 2: Implement logic to process user commands
def process_command(command):
    command_split = command.split(' ')
    return_command = []
    if command_split[0] == 'bars':
        location = ['sellcountry=', 'sellregion=', 'sourcecountry=', 'sourceregion=']
        sort = ['ratings', 'cocoa']
        limit = ['top=', 'bottom=']
        stat = 0
        loc = None
        sorter = ''
        lim = ''
        for x in command_split[1:]:
            if x in sort:
                sorter = x
            elif x[:4] == limit[0] or x[:7] == limit[1]:
                lim = x
            elif x[:12] == location[0] or x[:11] == location[1] or x[:14] == location[2] or x[:13] == location[3]:
                loc = x
            else:
                print('Invalid command! ' + command)
                stat = 1
                break
        if stat == 0:
            if sorter == '':
                sorter = 'ratings'
            if lim == '':
                lim = 'top=10'
            return_command = search_by_bar(sorter, lim, loc)
    elif command_split[0] == 'companies':
        stat = 0
        loc = None
        sorter = ''
        lim = ''
        location = ['country=', 'region=']
        sort = ['ratings', 'cocoa', 'bars_sold']
        limit = ['top=', 'bottom=']
        for x in command_split[1:]:
            if x[:8] == location[0] or x[:7] == location[1]:
                loc = x
            elif x in sort:
                sorter = x
            elif x[:4] == limit[0] or x[:7] == limit[1]:
                lim = x
            else:
                print('Invalid command! ' + command)
                stat = 1
                break
        if stat == 0:
            if sorter == '':
                sorter = 'ratings'
            if lim == '':
                lim = 'top=10'
            return_command = search_by_company(sorter, lim, loc)
    elif command_split[0] == 'countries':
        sellers = ['sellers', 'sources']
        sort = ['ratings', 'cocoa', 'bars_sold']
        limit = ['top=', 'bottom=']
        stat = 0
        loc = None
        seller = ''
        sorter = ''
        lim = ''
        for x in command_split[1:]:
            if x[:7] == 'region=':
                loc = x
            elif x in sellers:
                seller = x
            elif x in sort:
                sorter = x
            elif x[:4] == limit[0] or x[:7] == limit[1]:
                lim = x
            else:
                print('Invalid command! ' + command)
                stat = 1
                break
        if stat == 0:
            if sorter == '':
                sorter = 'ratings'
            if seller == '':
                seller = 'sellers'
            if lim == '':
                lim = 'top=10'
            return_command = search_by_country(seller, sorter, lim, loc)
    elif command_split[0] == 'regions':
        sellers = ['sellers', 'sources']
        sort = ['ratings', 'cocoa', 'bars_sold']
        limit = ['top=', 'bottom=']
        stat = 0
        seller = ''
        sorter = ''
        lim = ''
        for x in command_split[1:]:
            if x in sellers:
                seller = x
            elif x in sort:
                sorter = x
            elif x[:4] == limit[0] or x[:7] == limit[1]:
                lim = x
            else:
                print('Invalid command! ' + command)
                stat = 1
                break
        if stat == 0:
            if sorter == '':
                sorter = 'ratings'
            if seller == '':
                seller = 'sellers'
            if lim == '':
                lim = 'top=10'
            return_lst = search_by_region(seller, sorter, lim)
    else:
        print('Invalid command! ' + command)
    return return_command
    
def search_by_bar(sorter = 'ratings', lim = 'top=10', loc = None):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    argument = 'SELECT SpecificBeanBarName, Company, c.EnglishName AS CompanyLocation, Rating, Bars.CocoaPercent, c2.EnglishName AS BroadBeanOrigin FROM Bars JOIN Countries AS c ON CompanyLocationId = c.Id JOIN Countries AS c2 ON BroadBeanOriginId = c2.Id '
    if loc != None:
        argument += 'WHERE '
        if loc[:12] == 'sellcountry=':
            argument += 'c.Alpha2 = "' + str(loc[12:] + '" ')
        elif loc[:11] == 'sellregion=':
            argument += 'c.Region = "' + str(loc[11:] + '" ')
        elif loc[:14] == 'sourcecountry=':
            argument += 'c2.Alpha2 = "' + str(loc[14:] + '" ')
        elif loc[:13] == 'sourceregion=':
            argument += 'c2.Region = "' + str(loc[13:] + '" ')
    if sorter == 'ratings':
        argument += 'ORDER BY Rating '
    elif sorter == 'cocoa':
        argument += 'ORDER BY CocoaPercent '
    if lim[:4] == 'top=':
        argument += 'DESC LIMIT ' + str(lim[4:])
    elif lim[:7] == 'bottom=':
        argument += 'LIMIT ' + str(lim[7:])
    cur.execute(argument)
    bar_data = cur.fetchall()
    conn.close()
    return bar_data

def search_by_company(sorter = 'ratings', lim = 'top=10', loc = None):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    argument = 'SELECT Bars.Company, c.EnglishName AS CompanyLocation, '
    if sorter == 'ratings':
        argument += 'ROUND(AVG(Bars.Rating), 1) FROM Bars JOIN Countries AS c ON CompanyLocationId = c.Id GROUP BY Company HAVING COUNT(*) > 4 '
    elif sorter == 'cocoa':
        argument += 'ROUND(AVG(CocoaPercent), 2) FROM Bars JOIN Countries AS c ON CompanyLocationId = c.Id GROUP BY Company HAVING COUNT(*) > 4 '
    elif sorter == 'bars_sold':
        argument += 'COUNT(*) AS BarsSold FROM Bars JOIN Countries AS c ON CompanyLocationId = c.Id GROUP BY Company HAVING COUNT(*) > 4 '
    if loc != None:
        argument += 'AND '
        if loc[:8] == 'country=':
            argument += 'c.Alpha2 = "' + str(loc[8:] + '" ')
        elif loc[:7] == 'region=':
            argument += 'c.Region = "' + str(loc[7:] + '" ')
    if sorter == 'ratings':
        argument += 'ORDER BY AVG(Rating) '
    elif sorter == 'cocoa':
        argument += 'ORDER BY AVG(CocoaPercent) '
    elif sorter == 'bars_sold':
        argument += 'ORDER BY BarsSold '
    if lim[:4] == 'top=':
        argument += 'DESC LIMIT ' + str(lim[4:])
    elif lim[:7] == 'bottom=':
        argument += 'LIMIT ' + str(lim[7:])
    cur.execute(argument)
    company_data = cur.fetchall()
    conn.close()
    return company_data

def search_by_country(seller = 'sellers', sorter = 'ratings', lim = 'top=10', loc = None):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    argument = 'SELECT c.EnglishName, c.Region, '
    if sorter == 'ratings':
        argument += 'ROUND(AVG(Bars.Rating), 1) FROM Countries AS c JOIN Bars ON c.Id = Bars.'
        if seller == 'sellers':
            argument += 'CompanyLocationId GROUP BY CompanyLocationId HAVING COUNT(*) > 4 '
        elif seller == 'sources':
            argument += 'BroadBeanOriginId GROUP BY BroadBeanOriginId HAVING COUNT(*) > 4 '
    elif sorter == 'cocoa':
        argument += 'ROUND(AVG(CocoaPercent), 2) FROM Countries AS c JOIN Bars ON c.Id = Bars.'
        if seller == 'sellers':
            argument += 'CompanyLocationId GROUP BY CompanyLocationId HAVING COUNT(*) > 4 '
        elif seller == 'sources':
            argument += 'BroadBeanOriginId GROUP BY BroadBeanOriginId HAVING COUNT(*) > 4 '
    elif sorter == 'bars_sold':
        argument += 'COUNT(*) AS BarsSold FROM Countries AS c JOIN Bars ON c.Id = Bars.'
        if seller == 'sellers':
            argument += 'CompanyLocationId GROUP BY CompanyLocationId HAVING COUNT(*) > 4 '
        elif seller == 'sources':
            argument += 'BroadBeanOriginId GROUP BY BroadBeanOriginId HAVING COUNT(*) > 4 '
    if loc != None:
        argument += 'AND '
        if loc[:7] == 'region=':
            argument += 'c.Region = "' + str(loc[7:] + '" ')
    if sorter == 'ratings':
        argument += 'ORDER BY AVG(Rating) '
    elif sorter == 'cocoa':
        argument += 'ORDER BY AVG(CocoaPercent) '
    elif sorter == 'bars_sold':
        argument += 'ORDER BY BarsSold '
    if lim[:4] == 'top=':
        argument += 'DESC LIMIT ' + str(lim[4:])
    elif lim[:7] == 'bottom=':
        argument += 'LIMIT ' + str(lim[7:])
    cur.execute(argument)
    country_data = cur.fetchall()
    conn.close()
    return country_data

def search_by_region(seller = 'sellers', sorter = 'ratings', lim = 'top=10'):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    argument = 'SELECT c.Region, '
    if sorter == 'ratings':
        argument += 'ROUND(AVG(Rating), 1) FROM Countries AS c JOIN Bars ON c.Id = Bars.'
        if seller == 'sellers':
            argument += 'CompanyLocationId GROUP BY c.Region HAVING COUNT(*) > 4 '
        elif seller == 'sources':
            argument += 'BroadBeanOriginId GROUP BY c.Region HAVING COUNT(*) > 4 ORDER BY AVG(Rating) '
    elif sorter == 'cocoa':
        argument += 'ROUND(AVG(CocoaPercent), 2) FROM Countries AS c JOIN Bars ON c.Id = Bars.'
        if seller == 'sellers':
            argument += 'CompanyLocationId GROUP BY c.Region HAVING COUNT(*) > 4 '
        elif seller == 'sources':
            argument += 'BroadBeanOriginId GROUP BY c.Region HAVING COUNT(*) > 4 '
        statement += 'ORDER BY AVG(CocoaPercent) '
    elif sorter == 'bars_sold':
        argument += 'COUNT(*) AS BarsSold FROM Countries AS c JOIN Bars ON c.Id = Bars.'
        if seller == 'sellers':
            argument += 'CompanyLocationId GROUP BY c.Region HAVING COUNT(*) > 4 '
        elif seller == 'sources':
            argument += 'BroadBeanOriginId GROUP BY c.Region HAVING COUNT(*) > 4 '
        argument += 'ORDER BY BarsSold '
    if lim[:4] == 'top=':
        argument += 'DESC LIMIT ' + str(lim[4:])
    elif lim[:7] == 'bottom=':
        argument += 'LIMIT ' + str(lim[7:])
    cur.execute(argument)
    region_data = cur.fetchall()
    conn.close()
    return region_data

def load_help_text():
    with open('help.txt') as f:
        return f.read()
# Part 3: Implement interactive prompt. We've started for you!

def fix_function(tup):
    margins = []
    margin = 2
    for i in range(0, len(tup[0])):
        margins.append(column_length(tup, i))
    for x in tup:
        result = ''
        for i in range(0, len(x)):
            try:
                if float(row[i]) > 0 and float(x[i]) < 1:
                    out += str(int(float(x[i])*100)) + '%' + (margins[i] + margin - len(str(int(float(x[i])*100))) - 1) * ' '
                elif float(x[i]) >= 1:
                    out += str(x[i]) + (margins[i] + margin - len(str(x[i]))) * ' '
            except:
                result += str(x[i]) + (margins[i] + margin - len(str(x[i]))) * ' '
        print(result)
        
def column_length(tup, i):
    maximum_length = 0
    for x in tup:
        if len(str(x[i])) > maximum_length:
            maximum_length = len(str(x[i]))
    return maximum_length
    
def interactive_prompt():
    help_text = load_help_text()
    response = input('Enter a command: ')
    while response != 'exit':
        if response == 'help':
            print(help_text)
            response = input('Enter a command: ')
            continue
        else:
            command_list = process_command(response)
            try:
                fix_function(command_list)
            except:
                pass
        response = input('Enter a command: ')
    print('Thanks for using the program! Bye!')

# Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    interactive_prompt()
