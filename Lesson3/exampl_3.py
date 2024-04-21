import json

with open('../Lesson2/books_data.json', 'r') as file_read:
    file_str = json.load(file_read)
    for i in range(len(file_str)):
        file_str[i]['Price'] = float(file_str[i]['Price'].replace('£', ''))

with open('books_data_new.json', 'w') as f:
    json.dump(file_str, f, indent=4)






