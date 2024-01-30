import json
import csv
import requests
from bs4 import BeautifulSoup

url = "https://www.gov.kz/graphql"

languages = ['en', 'kk', 'ru']

items_dict = {}

def clean_text(text):
    if text is not None:
        cleaned_text = " ".join(text.split())
        soup = BeautifulSoup(cleaned_text, 'html.parser')
        return soup.get_text()
    else:
        return ""

for l in languages:
    headers = {
        'Accept-Language': l
    }
    body = """
    {
      projectdetails (_size:>0){
        id
        project_name 
        parent_govorg{
                id}
        class{
            name}
        phone
        contacts
        
      }
    }
    """
    r = requests.post(url=url, headers=headers, json={"query": body})
    data = json.loads(r.text)
    organizations = data['data']['projectdetails']

    for i in organizations:
        project_id = i['id']

        if i['class'] is None:
            i['class'] = {"id": "0","name": "0"}
        if i['parent_govorg'] is None:
            i['parent_govorg'] = {"id": "0", "project_name": "0"}

        i['contacts'] = clean_text(i['contacts'])

        if project_id not in items_dict:
            items_dict[project_id] = [
                project_id,
                i['parent_govorg']['id'],
                i['project_name'] if l == 'en' else None,
                i['project_name'] if l == 'kk' else None,
                i['project_name'] if l == 'ru' else None,
                i['class']['name'] if l == 'en' else None,
                i['class']['name'] if l == 'kk' else None,
                i['class']['name'] if l == 'ru' else None,
                i['phone'] ,
                i['contacts'] if l == 'en' else None,
                i['contacts'] if l == 'en' else None,
                i['contacts'] if l == 'en' else None
            ]
        else:
            items_dict[project_id][1 + languages.index(l)] = i['id']
            items_dict[project_id][2 + languages.index(l)] = i['project_name']
            items_dict[project_id][3 + languages.index(l)] = i['class']['name']
            items_dict[project_id][2 + languages.index(l)] = i['phone']
            items_dict[project_id][5 + languages.index(l)] = i['contacts']
            items_dict[project_id][5 + languages.index(l)] = clean_text(i['contacts'])

items_arr = list(items_dict.values())
print(items_arr)
header = ['id', 'Parent_id','Project_name_en', 'Project_name_kk', 'Project_name_ru',  'class_name_en','class_name_kk' ,'class_name_ru',
           'phone', 'contacts_en', 'contacts_kk', 'contacts_ru']

with open("Organizations.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=",",  quoting=csv.QUOTE_MINIMAL)
    w.writerow(header)
    w.writerows(items_arr)
