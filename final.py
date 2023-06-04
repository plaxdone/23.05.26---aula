import geopandas as gpd
import matplotlib, webbrowser, hdbscan, folium, re, warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import pandas as pd
import numpy as np
import seaborn as sns
from tqdm import tqdm
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.datasets import make_blobs
from sklearn.neighbors import KNeighborsClassifier
from ipywidgets import interactive
from collections import defaultdict

cols = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4',
        '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', 
        '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', 
        '#000075', '#808080']*100
sns.set(style="white")


final_df = pd.read_csv("./data/dataPR2.csv", na_values=[" "])
mun_geo = "./geoJson/new_munic.json"

geoJSON_df = gpd.read_file(mun_geo)

geoJSON_df = geoJSON_df.rename(columns = {"NOME":"customer_city"})
print(geoJSON_df)
print(final_df)
final_df = geoJSON_df.merge(final_df, on = "customer_city")

print(final_df.head())
# # função para criar map em diferentes classificadores

def create_map(df, cluster_column):
    m = folium.Map(location=[df.geolocation_lat.mean(), df.geolocation_lng.mean()], zoom_start=7, tiles='OpenStreet Map')

    for _, row in df.iterrows():

        if row[cluster_column] == -1:
            cluster_colour = '#000000'
        else:
            cluster_colour = cols[row[cluster_column]]

        folium.CircleMarker(
            location= [row['geolocation_lat'], row['geolocation_lng']],
            radius=5,
            popup= row[cluster_column],
            color=cluster_colour,
            fill=True,
            fill_color=cluster_colour
        ).add_to(m)
        
    return m

# # plota todas as localizações

'''
X = np.array(final_df[["geolocation_lng", "geolocation_lat"]], dtype='float64')
plt.scatter(X[:,0], X[:,1], alpha=0.2, s=50)
# plt.show()

m = folium.Map(location=[final_df.geolocation_lat.mean(), final_df.geolocation_lng.mean()], zoom_start=7, 
               tiles='OpenStreet Map')
for _, row in final_df.iterrows():
    folium.CircleMarker(
        location=[row.geolocation_lat, row.geolocation_lng],
        radius=5,
        color='#1787FE',
        fill=True,
        fill_colour='#1787FE'
    ).add_to(map)

map.save("map.html")
webbrowser.open("map.html")
'''

X_blobs, _ = make_blobs(n_samples=1000, centers=10, n_features=2, 
                        cluster_std=0.5, random_state=4)
plt.scatter(X_blobs[:,0], X_blobs[:,1], alpha=0.2)

# class_predictions = np.load('sample_clusters.npy')
# unique_clusters = np.unique(class_predictions)
# for unique_cluster in unique_clusters:
#     X = X_blobs[class_predictions==unique_cluster]
#     plt.scatter(X[:,0], X[:,1], alpha=0.2, c=cols[unique_cluster])

class_predictions = np.load('sample_clusters_improved.npy')
unique_clusters = np.unique(class_predictions)
for unique_cluster in unique_clusters:
    X = X_blobs[class_predictions==unique_cluster]
    plt.scatter(X[:,0], X[:,1], alpha=0.2, c=cols[unique_cluster])

# plt.show()






X_blobs, _ = make_blobs(n_samples=1000, centers=50, 
                        n_features=2, cluster_std=1, random_state=4)
data = defaultdict(dict)
for x in range(1,21):
    model = KMeans(n_clusters=3, random_state=17, 
                   max_iter=x, n_init=1).fit(X_blobs)
    
    data[x]['class_predictions'] = model.predict(X_blobs)
    data[x]['centroids'] = model.cluster_centers_
    data[x]['unique_classes'] = np.unique(class_predictions)

def f(x):
    class_predictions = data[x]['class_predictions']
    centroids = data[x]['centroids']
    unique_classes = data[x]['unique_classes']

    for unique_class in unique_classes:
            plt.scatter(X_blobs[class_predictions==unique_class][:,0], 
                        X_blobs[class_predictions==unique_class][:,1], 
                        alpha=0.3, c=cols[unique_class])
    plt.scatter(centroids[:,0], centroids[:,1], s=200, c='#000000', marker='v')
    plt.ylim([-15,15]); plt.xlim([-15,15])
    plt.title('How K-Means Clusters')
    #plt.show()

interactive_plot = interactive(f, x=(1, 20))
output = interactive_plot.children[-1]
output.layout.height = '350px'
interactive_plot

X = np.array(final_df[['geolocation_lat', 'geolocation_lng']], dtype='float64')
k = 70
model = KMeans(n_clusters=k, random_state=17).fit(X)
class_predictions = model.predict(X)
final_df[f'CLUSTER_kmeans{k}'] = class_predictions
final_df.to_csv("ver.csv")

## print(final_df.head())




m = create_map(final_df, 'CLUSTER_kmeans70')
# print(f'K={k}')
# print(f'Silhouette Score: {silhouette_score(X, class_predictions)}')

# m.save('kmeans_70.html')
# webbrowser.open("kmeans_70.html")

'''
best_silhouette, best_k = -1, 0

for k in tqdm(range(2, 100)):
    model = KMeans(n_clusters=k, random_state=1).fit(X)
    class_predictions = model.predict(X)
    
    curr_silhouette = silhouette_score(X, class_predictions)
    if curr_silhouette > best_silhouette:
        best_k = k
        best_silhouette = curr_silhouette
        
print(f'K={best_k}')
print(f'Silhouette Score: {best_silhouette}')
'''


dummy = np.array([-1, -1, -1, 2, 3, 4, 5, -1])

new = np.array([(counter+2)*x if x==-1 else x for counter, x in enumerate(dummy)])

model = DBSCAN(eps=0.01, min_samples=5).fit(X)
class_predictions = model.labels_

final_df['CLUSTERS_DBSCAN'] = class_predictions

m = create_map(final_df, 'CLUSTERS_DBSCAN')

    
# print(f'Number of clusters found: {len(np.unique(class_predictions))}')
# print(f'Number of outliers found: {len(class_predictions[class_predictions==-1])}')

# print(f'Silhouette ignoring outliers: {silhouette_score(X[class_predictions!=-1], class_predictions[class_predictions!=-1])}')

# no_outliers = 0
# no_outliers = np.array([(counter+2)*x if x==-1 else x for counter, x in enumerate(class_predictions)])
# print(f'Silhouette outliers as singletons: {silhouette_score(X, no_outliers)}')

# m.save('dbscan.html')
# webbrowser.open("dbscan.html")



model = hdbscan.HDBSCAN(min_cluster_size=5, min_samples=2, 
                        cluster_selection_epsilon=0.01)
# min_cluster_size
# min_samples
# cluster_slection_epsilon

class_predictions = model.fit_predict(X)
final_df['CLUSTER_HDBSCAN'] = class_predictions

m = create_map(final_df, 'CLUSTER_HDBSCAN')

# print(f'Number of clusters found: {len(np.unique(class_predictions))-1}')
# print(f'Number of outliers found: {len(class_predictions[class_predictions==-1])}')

# print(f'Silhouette ignoring outliers: {silhouette_score(X[class_predictions!=-1], class_predictions[class_predictions!=-1])}')

# no_outliers = np.array([(counter+2)*x if x==-1 else x for counter, x in enumerate(class_predictions)])
# print(f'Silhouette outliers as singletons: {silhouette_score(X, no_outliers)}')

# m.save('hdbscan.html')
# webbrowser.open("hdbscan.html")


'''
class_predictions = model.fit_predict(X)
final_df['CLUSTER_HDBSCAN'] = class_predictions

classifier = KNeighborsClassifier(n_neighbors=1)

df_train = final_df[final_df.CLUSTER_HDBSCAN!=-1]
df_predict = final_df[final_df.CLUSTER_HDBSCAN==-1]

X_train = np.array(final_df[['geolocation_lng', 'geolocation_lat']], dtype='float64')
y_train = np.array(final_df['CLUSTER_HDBSCAN'])

X_predict = np.array(df_predict[['geolocation_lng', 'geolocation_lat']], dtype='float64')

classifier.fit(X_train, y_train)

predictions = classifier.predict(X_predict)

final_df['CLUSTER_hybrid'] = final_df['CLUSTER_HDBSCAN']

final_df.loc[final_df.CLUSTER_HDBSCAN==-1, 'CLUSTER_hybrid'] = predictions

m = create_map(final_df, 'CLUSTER_hybrid')
m.save('dbscan.html')
webbrowser.open("dbscan.html")

class_predictions = final_df.CLUSTER_hybrid
print(f'Number of clusters found: {len(np.unique(class_predictions))}')
print(f'Silhouette: {silhouette_score(X, class_predictions)}')

m.save('hybrid.html')

'''