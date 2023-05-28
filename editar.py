import json
from unidecode import unidecode


# Opening JSON file
f = open('munic.json', encoding="utf-8")

data = json.load(f)
lista = []
  
for i in data['features']:
    i['properties']['NOME'] = unidecode(i['properties']['NOME'].lower())
    lista.append(i['properties']['NOME'])

# with open('new_munic.json', 'w') as f:
#     json.dump(data, f)
print(lista)



