import pandas as pd
from pyclustering.cluster.birch import birch
from pyclustering.cluster.kmeans import kmeans
from pyclustering.utils import read_sample;
from pyclustering.samples.definitions import FCPS_SAMPLES
from pyclustering.cluster import cluster_visualizer
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from sklearn.manifold import TSNE
import numpy as np
import sys
from pandas import DataFrame


train = pd.read_csv('/Users/xudunyuan/Desktop/data mining individual/web/trainData.csv')
labels = list(train.columns.values) #this is the first line of the csv file
total_column = train.shape[0]
total_row = train.shape[1]

total_num = [] #this 2D-array is for containing all value in the csv file
for i in range(0,total_column-1):
    num_df = train.iloc[i,:].values.tolist()
    num_df.pop(0)
    total_num.append(num_df)

X = np.array(total_num)
tsne = TSNE(n_components=2)
y = tsne.fit_transform(X)
print(tsne.embedding_)

wcss = []
for i in range(1, 80):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(y)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 80), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

kmeans = KMeans(n_clusters=30, init='k-means++', max_iter=300, n_init=10, random_state=0)
colors = ['b','g','r','orange']
pred_y = kmeans.fit_predict(y)
plt.scatter(y[:,0], y[:,1], s=3)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=100, c='red')
fig = plt.figure(figsize=(20,20))
plt.show()


data =DataFrame(total_num)

km = KMeans(n_clusters=5).fit(data)

cluster_map = pd.DataFrame()
cluster_map['data_index'] = data.index.values
cluster_map['cluster'] = km.labels_
cluster_map[cluster_map.cluster == 3]

all_clusters = []
for i in range(30):
    all_clusters.append(cluster_map[cluster_map.cluster == i]['data_index'].values.tolist())
all_clusters = np.array(all_clusters)