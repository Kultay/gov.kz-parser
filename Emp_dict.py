import json
import csv
import requests
from bs4 import BeautifulSoup
import re
from docx import Document


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
        cleaned_text = re.sub('[^a-zA-Zа-яА-ЯәғқңөұүhіӘҒҚҢӨҰҮҺІ0-9,.()-/@:;!№#$%&?*=_«» ]', '', text)
        return cleaned_text
    else:
        return None

def remove_map_symbol(text):
    if text is not None:
        cleaned_text = re.sub('[^0-9.,]', '', text)
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
        emp_dict{
                full_text{
                   document
                          }
                }
        
      }
    }
    """
    r = requests.post(url=url, headers=headers, json={"query": body})
    data = json.loads(r.text)
    organizations = data['data']['projectdetails']




    for i in organizations:
        project_id = i['id']

        if i['emp_dict'] is None:
            i['emp_dict'] = {"full_text":"0"}
        if i['emp_dict']['full_text'] is None:
            i['emp_dict']['full_text'] = {"document":"0"}

        if project_id not in items_dict:
            full_text = i['emp_dict']['full_text']

            if isinstance(full_text, dict):
                items_dict[project_id] = [full_text['document']]
            elif isinstance(full_text, str):

                items_dict[project_id] = [full_text]
            else:

                items_dict[project_id] = ["Unknown"]



items_arr = list(items_dict.values())

if items_arr is not None:
        print(items_arr)



header = ['document']

with open("document.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=",")
    w.writerow(header)
    w.writerows(items_arr)

