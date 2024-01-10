import pandas as pd
import json
import requests
import csv

url = "https://www.gov.kz/graphql"

headers = {
    'Accept-Language': 'ru'}

body = """
{
  projectdetails (_size:10){
    id
    project_name 
    supervisor{
                lastname_initials
                name}

  }
}
"""

r= requests.post(url=url, headers=headers,json={"query": body})
data = json.loads(r.text)

names = data['data']['projectdetails']




Headers = names[0].keys()
with open('data.file.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=Headers)
    writer.writeheader()
    for n in names:
        writer.writerow(n)




