import json
import csv
import requests

url = "https://www.gov.kz/graphql"

headers1 = {
    'Accept-Language': 'kk'}
headers2 = {
    'Accept-Language': 'ru'}
headers3 = {
    'Accept-Language': 'en'}

body = """
{
  projectdetails (_size:>1000){
    id
    project_name 
    supervisor{
                lastname_initials
                name
                lastname
                middlename
                position
                phone
                email}

  }
}
"""

r1 = requests.post(url=url, headers=headers1, json={"query": body})
r2 = requests.post(url=url, headers=headers2, json={"query": body})
r3 = requests.post(url=url, headers=headers3, json={"query": body})

data = json.loads(r1.text)
names1 = data['data']['projectdetails']

data = json.loads(r2.text)
names2 = data['data']['projectdetails']

data = json.loads(r3.text)
names3 = data['data']['projectdetails']

items_dict1 = {}

for i in range(len(names1)):
    if names1[i]['supervisor'] != None:
        items_dict1[names1[i]['id']] = [names1[i]['id'],
                                        names1[i]['project_name'],
                                        names1[i]['supervisor']['lastname_initials'],
                                        names1[i]['supervisor']['name'],
                                        names1[i]['supervisor']['lastname'],
                                        names1[i]['supervisor']['middlename'],
                                        names1[i]['supervisor']['position'],
                                        names1[i]['supervisor']['phone'],
                                        names1[i]['supervisor']['email']]
    else:
        pass

items_dict2 = {}

for i in range(len(names2)):
    if names2[i]['supervisor'] != None:
        items_dict2[names2[i]['id']] = [names2[i]['id'],
                                        names2[i]['project_name'],
                                        names2[i]['supervisor']['lastname_initials'],
                                        names2[i]['supervisor']['name'],
                                        names2[i]['supervisor']['lastname'],
                                        names2[i]['supervisor']['middlename'],
                                        names2[i]['supervisor']['position'],
                                        names2[i]['supervisor']['phone'],
                                        names2[i]['supervisor']['email']]
    else:
        pass

items_dict3 = {}

for i in range(len(names3)):
    if names3[i]['supervisor'] != None:
        items_dict3[names3[i]['id']] = [names3[i]['id'],
                                        names3[i]['project_name'],
                                        names3[i]['supervisor']['lastname_initials'],
                                        names3[i]['supervisor']['name'],
                                        names3[i]['supervisor']['lastname'],
                                        names3[i]['supervisor']['middlename'],
                                        names3[i]['supervisor']['position'],
                                        names3[i]['supervisor']['phone'],
                                        names3[i]['supervisor']['email']]
    else:
        pass

items_arr1 = list(items_dict1.values())
print(items_arr1)
header1 = ['id', 'Жоба_атауы', 'Аты_жөні', 'Аты', 'Тегі', 'Әкесінің_аты', 'Позиция', 'Телефон', 'Email']

items_arr2 = list(items_dict2.values())
print(items_arr1)
header2 = ['id', 'Имя_проекта', 'ФИО', 'Имя', 'Фамилия', 'Отчество', 'Позиция', 'Телефон', 'Email']

items_arr3 = list(items_dict3.values())
print(items_arr1)
header3 = ['id', 'Project_name', 'Lastname_initials', 'Name', 'Lastname', 'Middlename', 'Position', 'Phone', 'Email']

with open("stuff_kk.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter="|")
    w.writerow(header1)
    w.writerows(items_arr1)

with open("stuff_ru.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter="|")
    w.writerow(header2)
    w.writerows(items_arr2)

with open("stuff_en.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter="|")
    w.writerow(header3)
    w.writerows(items_arr3)
