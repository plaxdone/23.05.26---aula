import json
from unidecode import unidecode


# # Opening JSON file
# f = open('munic.json', encoding="utf-8")

# data = json.load(f)
# lista = []
  
# for i in data['features']:
#     i['properties']['NOME'] = unidecode(i['properties']['NOME'].lower())
#     lista.append(i['properties']['NOME'])

# # with open('new_munic.json', 'w') as f:
# #     json.dump(data, f)
# print(lista)

p = open('pop_mun.json', encoding="utf-8")

data = json.load(p)

# dict = {}
# for i in data[0]['resultados'][0]['series']:
#     cidade = unidecode(i['localidade']['nome'].split(' ')[0]).lower()
#     pop = (i['serie']['2007'])
#     dict[cidade] = pop
# # print(dict)

# with open("sample.json", "w") as outfile:
#     json.dump(dict, outfile)

import csv
with open('teste.csv', 'w') as csvfile:
    csv.writer(csvfile, delimiter=',').writerow(['customer_city', 'pop'])
    for i in data[0]['resultados'][0]['series']:
        cidade = unidecode(i['localidade']['nome'].split(' ')[0]).lower()
        pop = (i['serie']['2007'])
        csv.writer(csvfile, delimiter=',').writerow([cidade, pop])
