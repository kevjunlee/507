import json
# 507 Homework 7 Part 2

count = 0
#### Your Part 2 solution goes here ####
f = open('directory_dict.json', 'r')
directory_data = f.read()
new_directory_data = json.loads(directory_data)
f.close()

for i in new_directory_data:
    if new_directory_data[i]["title"] == "PhD student":
        count += 1
#### Your answer output (change the value in the variable, count)####
print('The number of PhD students: ', count)
