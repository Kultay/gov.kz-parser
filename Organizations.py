import json
import csv
import requests

url = "https://www.gov.kz/graphql"

languages = ['en', 'kk', 'ru']

items_dict = {}

for l in languages:
    headers = {
        'Accept-Language': l
    }
    body = """
    {
      projectdetails (_size:>0){
        id
        project_name 
        supervisor {
          lastname_initials
          name
          lastname
          middlename
          position
          phone
          email
        }
      }
    }
    """
    r = requests.post(url=url, headers=headers, json={"query": body})
    data = json.loads(r.text)
    organizations = data['data']['projectdetails']

    for i in organizations:
        project_id = i['id']
        if i['supervisor'] is None:
            i['supervisor'] = {"lastname_initials": "0", "name": "0", "lastname": "0", "middlename": "0",
                               "position": "0", "phone": "0", "email": "0"}

        if project_id not in items_dict:
            items_dict[project_id] = [
                project_id,
                i['project_name'] if l == 'en' else None,
                i['project_name'] if l == 'kk' else None,
                i['project_name'] ,
                i['supervisor']['lastname_initials'],
                i['supervisor']['name'],
                i['supervisor']['lastname'],
                i['supervisor']['middlename'],
                i['supervisor']['position'],
                i['supervisor']['phone'],
                i['supervisor']['email']
            ]
        else:
            items_dict[project_id][1 + languages.index(l)] = i['project_name']
            items_dict[project_id][2 + languages.index(l)] = i['supervisor']['lastname_initials']
            items_dict[project_id][3 + languages.index(l)] = i['supervisor']['name']
            items_dict[project_id][4 + languages.index(l)] = i['supervisor']['lastname']
            items_dict[project_id][5 + languages.index(l)] = i['supervisor']['middlename']
            items_dict[project_id][6 + languages.index(l)] = i['supervisor']['position']
            items_dict[project_id][7 + languages.index(l)] = i['supervisor']['phone']
            items_dict[project_id][8 + languages.index(l)] = i['supervisor']['email']


items_arr = list(items_dict.values())
print(items_arr)
header = ['id', 'Project_name_en', 'Project_name_kk', 'Project_name_ru', 'Lastname_initials', 'Name', 'Lastname',
          'Middlename', 'Position', 'Phone', 'Email']

with open("Organizations.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=",")
    w.writerow(header)
    w.writerows(items_arr)
