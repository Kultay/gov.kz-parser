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
        cleaned_text = re.sub('[^a-zA-Zа-яА-ЯәғқңөұүhіӘҒҚҢӨҰҮҺІ0-9,.()-/@:; ]', '', text)
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
        project_name 
        supervisor {
          lastname_initials
          lastname
          name
          middlename
          position
          phone
          email
          biography
          biography_details
        }
      }
    }
    """
    r = requests.post(url=url, headers=headers, json={"query": body})
    data = json.loads(r.text)
    organizations = data['data']['projectdetails']

    for i in organizations:
        project_id = i['id']

        # Replace with zero
        if i['supervisor'] is None:
            i['supervisor'] = {"lastname_initials": "0", "lastname": "0", "name": "0", "middlename": "0",
                               "position": "0", "phone": "0", "email": "0", "biography": "0", "biography_details": "0"}

        # Clean text
        i['supervisor']['biography'] = clean_text(i['supervisor']['biography'])
        i['supervisor']['biography_details'] = clean_text(i['supervisor']['biography_details'])

        #Remove symbol
        i['project_name'] = remove_symbol(i['project_name'])
        i['supervisor']['lastname_initials'] = remove_symbol(i['supervisor']['lastname_initials'])
        i['supervisor']['lastname'] = remove_symbol(i['supervisor']['lastname'])
        i['supervisor']['name'] = remove_symbol(i['supervisor']['name'])
        i['supervisor']['middlename'] = remove_symbol(i['supervisor']['middlename'])
        i['supervisor']['position'] = remove_symbol(i['supervisor']['position'])
        i['supervisor']['phone'] = remove_symbol(i['supervisor']['phone'])
        i['supervisor']['email'] = remove_symbol(i['supervisor']['email'])
        i['supervisor']['biography'] = remove_symbol(i['supervisor']['biography'])
        i['supervisor']['biography_details'] = remove_symbol(i['supervisor']['biography_details'])

        # Fill out the dictionary in different languages
        if project_id not in items_dict:
            items_dict[project_id] = [
                project_id,
                i['project_name'] if l == 'en' else None,
                i['project_name'] if l == 'kk' else None,
                i['project_name'] if l == 'ru' else None,
                i['supervisor']['lastname_initials'] if l == 'ru' else None,
                i['supervisor']['lastname'] if l == 'ru' else None,
                i['supervisor']['name'] if l == 'ru' else None,
                i['supervisor']['middlename'] if l == 'ru' else None,
                i['supervisor']['position'] if l == 'ru' else None,
                i['supervisor']['phone'],
                i['supervisor']['email'],
                i['supervisor']['biography'] if l == 'ru' else None,
                i['supervisor']['biography_details'] if l == 'ru' else None
            ]
        else:
            items_dict[project_id][1 + languages.index(l)] = i['project_name']
            items_dict[project_id][2 + languages.index(l)] = i['supervisor']['lastname_initials']
            items_dict[project_id][3 + languages.index(l)] = i['supervisor']['lastname']
            items_dict[project_id][4 + languages.index(l)] = i['supervisor']['name']
            items_dict[project_id][5 + languages.index(l)] = i['supervisor']['middlename']
            items_dict[project_id][6 + languages.index(l)] = i['supervisor']['position']
            items_dict[project_id][7 + languages.index(l)] = i['supervisor']['phone']
            items_dict[project_id][8 + languages.index(l)] = i['supervisor']['email']
            items_dict[project_id][9 + languages.index(l)] = i['supervisor']['biography']
            items_dict[project_id][10 + languages.index(l)] = i['supervisor']['biography_details']
            items_dict[project_id][9 + languages.index(l)] = clean_text(i['supervisor']['biography'])
            items_dict[project_id][10 + languages.index(l)] = clean_text(i['supervisor']['biography_details'])

items_arr = list(items_dict.values())

header = ['id', 'Project_name_en', 'Project_name_kk', 'Project_name_ru', 'Lastname_initials', 'lastname', 'Name',
          'Middlename', 'Position', 'Phone', 'Email', 'Biography', 'biography_details']

with open("supervisors.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=",")
    w.writerow(header)
    w.writerows(items_arr)