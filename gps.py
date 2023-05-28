import pandas as pd
import numpy as np
import webbrowser

file_url = "dataPRCWB.csv"
data = pd.read_csv(file_url)
features = data[['geolocation_lat', 'geolocation_lng']]
X = np.array(features)
# print(X[:10])

from k_means_constrained import KMeansConstrained
clf = KMeansConstrained(
    n_clusters=16,
    size_min=56,
    size_max=256,
    random_state=0
)
clf.fit_predict(X)
# save results
labels = clf.labels_
# send back into dataframe and display it
data['cluster'] = labels
# display the number of mamber each clustering
_clusters = data.groupby('cluster')['customer_id'].count()
print(_clusters)

import folium
colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', \
     'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', \
     'darkpurple', 'pink', 'lightblue', 'lightgreen', 'gray', \
     'black', 'lightgray', 'red', 'blue', 'green', 'purple', \
     'orange', 'darkred', 'lightred', 'beige', 'darkblue', \
     'darkgreen', 'cadetblue', 'darkpurple','pink', 'lightblue', \
     'lightgreen', 'gray', 'black', 'lightgray' ]
geolocation_lat = data.iloc[0]['geolocation_lat']
geolocation_lng = data.iloc[0]['geolocation_lng']
map = folium.Map(location=[geolocation_lng, geolocation_lat], zoom_start=12)
for _, row in data.iterrows():
    folium.CircleMarker(
        location=[row["geolocation_lng"], row["geolocation_lat"]],
        radius=12, 
        weight=2, 
        fill=True, 
        fill_color=colors[int(row["cluster"])],
        color=colors[int(row["cluster"])]
    ).add_to(map)

map.save("map.html")
webbrowser.open("map.html")