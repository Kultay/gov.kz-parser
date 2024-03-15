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
        cleaned_text = re.sub('[^a-zA-Zа-яА-ЯәғқңөұүhіӘҒҚҢӨҰҮҺІ0-9,.()-/@:;!№#$%&?*=_ ]', '', text)
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
        supervisors {
          id
          order
          lastname_initials
          lastname
          name
          middlename
          position
          phone
          email
          social_media{
          link}
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
        for supervisors in i['supervisors']:
            supervisors_id = supervisors['id']

            # Replace with zero
            if supervisors is not None:
                i['supervisors'] = {"order": "0", "lastname_initials": "0", "lastname": "0", "name": "0", "middlename": "0",
                                    "position": "0", "phone": "0", "email": "0", "biography": "0", "biography_details": "0"}

            # Clean text
            supervisors['order'] = str(supervisors['order'])
            supervisors['biography'] = clean_text(supervisors['biography']).strip()
            supervisors['biography_details'] = clean_text(supervisors['biography_details']).strip()

            # Remove symbol
            supervisors['lastname_initials'] = remove_symbol(supervisors['lastname_initials'])
            supervisors['lastname'] = remove_symbol(supervisors['lastname'])
            supervisors['name'] = remove_symbol(supervisors['name'])
            supervisors['middlename'] = remove_symbol(supervisors['middlename'])
            supervisors['position'] = remove_symbol(supervisors['position'])
            supervisors['phone'] = remove_symbol(supervisors['phone'])
            supervisors['email'] = remove_symbol(supervisors['email'])
            supervisors['biography'] = remove_symbol(supervisors['biography'])
            supervisors['biography_details'] = remove_symbol(supervisors['biography_details'])

            # Fill out the dictionary in different languages
            if supervisors_id is not items_dict:
                items_dict[supervisors_id] = [
                    i['id'],
                    supervisors_id,
                    supervisors['order'] ,
                    supervisors['lastname_initials'] if l == 'ru' else None,
                    supervisors['lastname'] if l == 'ru' else None,
                    supervisors['name'] if l == 'ru' else None,
                    supervisors['middlename'] if l == 'ru' else None,
                    supervisors['position'] if l == 'ru' else None,
                    supervisors['phone'],
                    supervisors['email'],
                    supervisors['biography'] if l == 'ru' else None,
                    supervisors['biography_details'] if l == 'ru' else None,
                ]


items_arr = list(items_dict.values())

header = ['Projects_id','Supervisors_id' ,'Order','Lastname_initials', 'lastname', 'Name',
          'Middlename', 'Position', 'Phone', 'Email','Biography', 'biography_details']

with open("supervisors.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=",")
    w.writerow(header)
    w.writerows(items_arr)