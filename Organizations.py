import json
import csv
import requests
from bs4 import BeautifulSoup
import re

url = "https://www.gov.kz/graphql"

languages = ['en', 'kk', 'ru']

items_dict = {}

# Clean text function
def clean_text(text):
    if text is not None:
        if any(tag in text for tag in ['<', '>']):
            cleaned_text = " ".join(text.split())
            soup = BeautifulSoup(cleaned_text, 'html.parser')
            return soup.get_text()
        else:
            return text.strip()
    else:
        return ""

# Remove symbol function
def remove_symbol(text):
    if text is not None:
        cleaned_text = re.sub('[^a-zA-Zа-яА-ЯәғқңөұүhіӘҒҚҢӨҰҮҺІ0-9,.()-/@:;!№#$%&?*= ]', '', text)
        return cleaned_text
    else:
        return None

# Request of Postman
for l in languages:
    headers = {
        'Accept-Language': l
    }
    body = """
    {
      projectdetails (_size:>0){
        id
        parent_govorg{
                id}
        project_name 
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

        # Replace with zero
        if i['class'] is None:
            i['class'] = {"id": "0", "name": "0"}
        if i['parent_govorg'] is None:
            i['parent_govorg'] = {"id": "0", "project_name": "0"}

        # Clean text
        i['contacts'] = clean_text(i['contacts'])

        # Remove symbol
        i['contacts'] = remove_symbol(i['contacts'])
        i['project_name'] = remove_symbol(i['project_name'])
        i['class']['name'] = remove_symbol(i['class']['name'])
        i['phone'] = remove_symbol(i['phone'])

        # Fill out the dictionary in different languages
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
                i['phone'],
                i['contacts'] if l == 'ru' else None
            ]
        else:
            items_dict[project_id][2 + languages.index(l)] = i['project_name']
            items_dict[project_id][5 + languages.index(l)] = i['class']['name']
            items_dict[project_id][6 + languages.index(l)] = i['phone']
            items_dict[project_id][7 + languages.index(l)] = i['contacts']
            items_dict[project_id][7 + languages.index(l)] = clean_text(i['contacts'])

items_arr = list(items_dict.values())

header = ['id', 'Parent_id','Project_name_en', 'Project_name_kk', 'Project_name_ru',  'class_name_en','class_name_kk' ,'class_name_ru',
           'phone', 'contacts_ru']

with open("Organizations.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=",", )
    w.writerow(header)
    w.writerows(items_arr)