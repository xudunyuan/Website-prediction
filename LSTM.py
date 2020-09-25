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


a = []
train = pd.read_csv('/Users/xudunyuan/Desktop/data mining individual/web/trainData.csv')
#test = pd.read_csv('trainData.csv')

labels = list(train.columns.values) #this is the first line of the csv file
total_column = train.shape[0]
total_row = train.shape[1]

for i in range(1,len(labels)):
	column = train[labels[i]].tolist()
	Num_vote = 0
	for j in range(0,len(column)):
		Num_vote+=column[j]
	a.append(Num_vote)

lessThan5=[]
for i in range(0, len(a)):
	if a[i] <=5 :
		lessThan5.append(i)
new = train
for i in lessThan5:
	new = new.drop([labels[i+1]],axis=1)

train = new
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

kmeans = KMeans(n_clusters=30, init='k-means++', max_iter=300, n_init=10, random_state=0)
pred_y = kmeans.fit_predict(y)

data =DataFrame(y)

km = KMeans(n_clusters=30).fit(data)

cluster_map = pd.DataFrame()
cluster_map['data_index'] = data.index.values
cluster_map['cluster'] = km.labels_

total_cluster=[]
for j in range(20):
    cluster = []
    for i in cluster_map[cluster_map.cluster == j].values.tolist():
        cluster.append(i[0])
    total_cluster.append(cluster)

all_sum = [] # 2_D list contains all value
for k in range(0,20):
	cluster_num = [] #2-D list contain k th cluster
	for i in total_cluster[k]:
	    cluster_num.append(total_num[i])
	sum_=[]
	for j in range(0,len(labels)-1): # calculate how many 1s in each column in this cluster
	    sum1 = 0
	    for m in range(0, len(cluster_num)):
	        sum1 = sum1 + cluster_num[m][j]
	    sum_.append(sum1)
	all_sum.append(sum_)

all_prob = []
for k in range(0, len(all_sum)):
    pr = []
    total = 0
    for i in range(0, len(labels)-1):
        total = total + all_sum[k][i]
    for i in range(0, len(labels)-1):
        prob = float(all_sum[k][i]) / total
        pr.append(prob)
    all_prob.append(pr)
p = DataFrame(all_prob)