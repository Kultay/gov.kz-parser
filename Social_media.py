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
      social_media(_size:>0){
        id
        projects
        title
        sm{
          name}
        url
        
    }
    }
    """
    r = requests.post(url=url, headers=headers, json={"query": body})
    data = json.loads(r.text)
    SocialMedia = data['data']['social_media']

    for i in SocialMedia:
        SocialMedia_id = i['id']


        i['projects'] =clean_text(i['projects'])


        i['projects'] = remove_projects_symbol(i['projects'])
        i['title'] = remove_symbol(i['title'])
        i['url'] = remove_symbol(i['url'])

        if SocialMedia_id not in items_dict:
            items_dict[SocialMedia_id] = [
                SocialMedia_id,
                i['projects'],
                i['title'],
                i['sm']['name'],
                i['url']
            ]

items_arr = list(items_dict.values())

headers = [ "id", "projects(slug)","title", "name","url" ]

with open ("Social_media.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=',')
    w.writerow(headers)
    w.writerows(items_arr)



