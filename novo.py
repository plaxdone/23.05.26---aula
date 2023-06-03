import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np

from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.neighbors import KNeighborsClassifier

import hdbscan
import folium
import re
from random import randint

def colors(x):
    opc = []
    n = 3
    for i in range(x):
        opc.append('#%06X' % randint(0, 0xFFFFFF))
    return opc

data=pd.read_csv("./data/locPri.csv")
data=pd.read_csv("./data/dataPR2.csv")
#print(data.head())

# plot lat x lon dos dados

X=np.array(data[['price']],dtype='float64')
# plt.scatter(X[:,0],X[:,1],alpha=0.2,s=50)
# plt.grid(True)
# plt.show()

# # plot todos os pontos no mapa

# plt_map=folium.Map(location=[data.geolocation_lat.mean(),data.geolocation_lng.mean()],zoom_start=7,
#              tiles='OpenStreetMap')
# for _,row in data.iterrows():
#     folium.CircleMarker(
#         location=[row.geolocation_lat,row.geolocation_lng],
#         radius=5,
#         color='blue',
#         fill=True
#     ).add_to(plt_map)
# plt_map.show_in_browser()

k_range=range(5,150,5) # (x, y, z) incremente de x a y incrementando z
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

k=int((best_k + best_inertia)//2)
print(f'best k - {best_k}')
print(f'best inertia - {best_inertia}')
print(f' k - {k}')
model=KMeans(n_clusters=k,random_state=17).fit(X)
pred=model.predict(X)
data[f'CLUSTER_kmeans']=pred

def create_map(data,cluster_col):
    m = folium.Map(location=[data.geolocation_lat.mean(), data.geolocation_lng.mean()], zoom_start=7, tiles='openstreetmap')
    cols = colors(k)
    for _, row in data.iterrows():

        # get a colour
        if row[cluster_col]==-1:
            cluster_colour='black'
        else:
            cluster_colour = cols[row[cluster_col]]

        folium.CircleMarker(
            location=[row.geolocation_lat,row.geolocation_lng],
            radius=5,
            popup= row['price'],
            color=cluster_colour,
            fill=True,
            fill_color=cluster_colour
        ).add_to(m)
    return m

plt_map=create_map(data,'CLUSTER_kmeans')   
# print(f'Silhouette Score: {silhouette_score(X, pred)}')
plt_map.save('kmeans_map.html')
plt_map.show_in_browser()