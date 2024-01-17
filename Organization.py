import json
import csv
import requests

url = "https://www.gov.kz/graphql"

languages = ['en', 'ru', 'kk']

item = []

for l in languages:
    headers = {
        'Accept-Language': l}
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
    r = requests.post(url=url, headers=headers, json={"query": body})
    data = json.loads(r.text)
    names = data['data']['projectdetails']
    item.append(names)

items = item[0] + item[1] + item[2]

items_dict = {}

for i in range(len(items)):
    if items[i]['supervisor'] != None:
        items_dict[items[i]['project_name']] = [items[i]['project_name'],
                                      items[i]['id'],
                                      items[i]['supervisor']['lastname_initials'],
                                      items[i]['supervisor']['name'],
                                      items[i]['supervisor']['lastname'],
                                      items[i]['supervisor']['middlename'],
                                      items[i]['supervisor']['position'],
                                      items[i]['supervisor']['phone'],
                                      items[i]['supervisor']['email']]


    else:
        pass

items_arr1 = list(items_dict.values())
print(items_arr1)
header = ['Project_name', 'id', 'Lastname_initials', 'Name', 'Lastname', 'Middlename', 'Position', 'Phone', 'Email']

with open("stuff.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter="|")
    w.writerow(header)
    w.writerows(items_arr1)







    for name in names:
        for i in range(len(names)):
            if name['id'] == names[i]['id']:
                if l == 'en':
                    name['project_name_en'] = name.pop('project_name')
                elif l == 'ru':
                    name['project_name_ru'] = name.pop('project_name')
                else:
                    name['project_name_kk'] = name.pop('project_name')
    items.append(names)

print(items)


