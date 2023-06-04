import json, folium, warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
from random import randint
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# # 41 19509 05 00 0029
# # xx = UF
# # xxxxx = Municípior
# # xx = Distrito
# # xx = Subdistrito
# # xxxx = Setor

def colors(x):
    opc = []
    n = 3
    for i in range(x):
        opc.append('#%06X' % randint(0, 0xFFFFFF))
    return opc

df = pd.read_csv('./rendaIBGE/cep_coordinates_per_capita_income.csv')
temp = df['CD_GEOCODI']
lista = []
for it in temp:
    lista.append(int(str(it)[:7]))
df['id_munic'] = lista
#print(df)
cidades = open('./rendaIBGE/municipios.json', encoding="utf-8")
cidades = json.load(cidades)
cidades = pd.DataFrame(cidades)
#print(cidades['id'])

df = cidades.merge(df, how='inner', left_on='id', right_on='id_munic')

df = df[['LAT','LON','renda_per_capita','nome']]
df = df.rename(columns = {'LAT':'Latitude','LON':'Longitude','renda_per_capita':'Renda','nome':'Cidade'})

# print(df)

X=np.array(df[['Renda']],dtype='float64')

# print(X)

k_range=range(2,20,1) # (x, y, z) incremente de x a y incrementando z
kmeans_per_k=[]
for k in k_range:
    kmeans=KMeans(n_clusters=k,random_state=42).fit(X)
    kmeans_per_k.append(kmeans)

silh_scores=[silhouette_score(X,model.labels_) for model in kmeans_per_k]
best_index = np.argmax(silh_scores)
best_k = k_range[best_index]
best_score = silh_scores[best_index]
# print("best k value:",best_k)
# print("silhouette score:",best_score)

# plt.figure(figsize=(8, 3))
# plt.grid(True)
# plt.plot(k_range, silh_scores, "bo-")
# plt.xlabel("k", fontsize=14)
# plt.ylabel("Silhouette score", fontsize=14)
# plt.plot(best_k, best_score, "rs")
# plt.show()

inertias = [model.inertia_ for model in kmeans_per_k]
best_inertia = inertias[best_index]

# plt.figure(figsize=(8, 3.5))
# plt.grid(True)
# plt.plot(k_range, inertias, "bo-")
# plt.xlabel("$k$", fontsize=14)
# plt.ylabel("Inertia", fontsize=14)
# plt.plot(best_k, best_inertia, "rs")
# plt.show()

k=10 #int((best_k + best_inertia)//2)
print(f'best k - {best_k}')
print(f'best inertia - {best_inertia}')
print(f' k - {k}')
model=KMeans(n_clusters=k,random_state=17).fit(X)
pred=model.predict(X)
df[f'CLUSTER_kmeans']=pred

def create_map(data,cluster_col):
    m = folium.Map(location=[data.Latitude.mean(), data.Longitude.mean()], zoom_start=10, tiles='openstreetmap')
    cols = colors(k)
    for _, row in data.iterrows():

        # get a colour
        if row[cluster_col]==-1:
            cluster_colour='black'
        else:
            cluster_colour = cols[row[cluster_col]]

        folium.CircleMarker(
            location=[row.Latitude,row.Longitude],
            radius=3,
            popup= row['Renda'],
            color=cluster_colour,
            fill=True,
            fill_color=cluster_colour
        ).add_to(m)
    return m

plt_map=create_map(df,'CLUSTER_kmeans')   
# print(f'Silhouette Score: {silhouette_score(X, pred)}')
# plt_map.save('kmeans_map.html')
plt_map.show_in_browser()