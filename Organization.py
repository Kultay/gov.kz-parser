import json
import csv
import requests

url = "https://www.gov.kz/graphql"

languages = ['en', 'ru', 'kk']

items_dict = {}

for l in languages:
    headers = {
        'Accept-Language': l
    }
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
          email
        }
      }
    }
    """
    r = requests.post(url=url, headers=headers, json={"query": body})
    data = json.loads(r.text)
    organizations = data['data']['projectdetails']

    for i in organizations:
        if i['supervisor'] is not None:
            project_id = i['id']
            if project_id not in items_dict:
                items_dict[project_id] = [
                    project_id,
                    i['project_name'] if l == 'en' else None,
                    i['project_name'] if l == 'kk' else None,
                    i['project_name'] if l == 'ru' else None,
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

items_arr = list(items_dict.values())
header = ['id', 'Project_name_en', 'Project_name_ru', 'Project_name_kk', 'Lastname_initials', 'Name', 'Lastname',
          'Middlename', 'Position', 'Phone', 'Email']


with open("Organizations.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=",")
    w.writerow(header)
    w.writerows(items_arr)