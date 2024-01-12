import json
import csv
import requests

url = "https://www.gov.kz/graphql"

languages = ['en', 'ru', 'kk']

item = []

for l in languages:
    headers = {
        'Accept-Language': l}
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
                    email}

      }
    }
    """
    r = requests.post(url=url, headers=headers, json={"query": body})
    data = json.loads(r.text)
    names = data['data']['projectdetails']
    item.append(names)













