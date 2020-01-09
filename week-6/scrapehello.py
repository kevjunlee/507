
from bs4 import BeautifulSoup

f = open("hello.html")
html = f.read()
soup = BeautifulSoup(html, 'html.parser')

# print(soup.prettify())

# searching by tag
all_list_items = soup.find_all('li')
all_divs = soup.find_all('div')

# searching by class
all_goodbye_elements = soup.find_all(class_='goodbye')

# searching by tag AND class
all_french_list_items = soup.find_all('li', class_='french')

# searching by id
all_hello_elements = soup.find_all(id='hello-list')

print('list items:', all_list_items)
print('------')
print('divs:', all_divs)
print('------')
print('goodbye elements:', all_goodbye_elements)
print('------')
print('french stuff:', all_french_list_items)
print('------')
print('hello id elements:', all_hello_elements)
print('------')

print(type(all_list_items[0]))
print('------')

print('All list items:')
for li in all_list_items:
  print(li.string)
print('------')

print('Children of hello-list:')
for child in all_hello_elements[0].children:
  print(child.string)
print('------')

print('List items within the hello tag')
hello_list_items = all_hello_elements[0].find_all('li')
print (hello_list_items)
print('------')

print('The hello-list element')
the_hello_element = soup.find(id='hello-list')
print(the_hello_element)
print('------')

img_tag = soup.find('img')
print('The img source:')
print(img_tag['src'])
print('------')

def get_goodbye():
    soupie = BeautifulSoup(html, features='html.parser')
    goodbyelist = []
    for goodbye in soupie.findAll('li'):
        goodbyelist.append(goodbye.string)
    print(goodbyelist[5:10])
    
get_goodbye()
