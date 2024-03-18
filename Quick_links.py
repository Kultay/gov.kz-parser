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

def remove_projects_symbol(text):
    if text is not None:
        cleaned_text = re.sub('[^a-zA-Z- ]', '', text)
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
      quick_links (_size:>0){
        id
        projects
        title
        external_link
        internal_link

      }
    }
    """
    r = requests.post(url=url, headers=headers, json={"query": body})
    data = json.loads(r.text)
    QuickLinks = data['data']['quick_links']

    for i in QuickLinks:
        QuickLinks_id = i['id']

        i['projects'] = clean_text(i['projects'])


        i['projects'] = remove_projects_symbol(i['projects'])
        i['title'] = remove_symbol(i['title'])
        i['external_link'] = remove_symbol(i['external_link'])
        i['internal_link'] = remove_symbol(i['internal_link'])

        if QuickLinks_id not in items_dict:
            items_dict[QuickLinks_id] = [
                QuickLinks_id,
                i['projects'],
                i['title'] if l == 'en' else None,
                i['title'] if l == 'kk' else None,
                i['title'] if l == 'ru' else None,
                i['external_link'],
                i['internal_link']
            ]
        else:
            items_dict[QuickLinks_id][2 + languages.index(l)] = i['title']
            items_dict[QuickLinks_id][3 + languages.index(l)] = i['external_link']
            items_dict[QuickLinks_id][4 + languages.index(l)] = i['internal_link']

items_arr = list(items_dict.values())

headers = ["id", "projects(slug)", "title_en", "title_kk", "title_ru", "external_link", "internal_link"]

with open("Quick_links.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=',')
    w.writerow(headers)
    w.writerows(items_arr)