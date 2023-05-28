import pandas as pd
file_url = "dataPRCWB.csv"
data = pd.read_csv(file_url)
features = data[['geolocation_lat', 'geolocation_lng']]
# print(features)

from sklearn.cluster import KMeans
# create kmeans model/object
kmeans = KMeans(
    init="random",
    n_clusters=16,
    n_init=10,
    max_iter=300,
    random_state=42
)

# do clustering
kmeans.fit(features)
# save results
labels = kmeans.labels_

# send back into dataframe and display it
data['cluster'] = labels
# display the number of mamber each clustering
_clusters = data.groupby('cluster')['customer_id'].count()
print(_clusters)
# _clusters.to_csv("gps.csv")