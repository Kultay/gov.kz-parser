import json
import csv
import requests


url = "https://www.gov.kz/graphql"

headers = {
    'Accept-Language': 'ru-RU,ru;q=0.9'}

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

r = requests.post(url=url, headers=headers,json={"query": body})

data = json.loads(r.text)
names = data['data']['projectdetails']





items_dict = {}

for i in range(len(names)):
    if names[i]['supervisor'] != None:
        items_dict[names[i]['id']] = [names[i]['id'],
                                      names[i]['project_name'],
                                      names[i]['supervisor']['lastname_initials'],
                                      names[i]['supervisor']['name'],
                                      names[i]['supervisor']['lastname'],
                                      names[i]['supervisor']['middlename'],
                                      names[i]['supervisor']['position'],
                                      names[i]['supervisor']['phone'],
                                      names[i]['supervisor']['email']]
    else:
        pass





items_arr = list(items_dict.values())
print(items_arr)
header = ['id','project_name','lastname_initials' , 'name','lastname','middlename','position','phone','email' ]

with open("stuff.csv", "w", newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter="|")
    w.writerow(header)
    w.writerows(items_arr)










