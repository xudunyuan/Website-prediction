import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import sys
import graphviz

train = pd.read_csv('/Users/xudunyuan/Desktop/data mining individual/web/trainData.csv')
labels = list(train.columns.values) #this is the first line of the csv file
total_column = train.shape[0]
total_row = train.shape[1]

total_num = [] #this 2D-array is for containing all value in the csv file
for i in range(0,total_column-1):
    num_df = train.iloc[i,:].values.tolist()
    num_df.pop(0)
    total_num.append(num_df)
pca=PCA(n_components=2)
newData=pca.fit_transform(total_num)
#newData is the lowD data produced by PCA method

wcss = []
for i in range(1, 80):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(newData)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 80), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()
#here we draw a picture that could show the curve when changing number of clusters

kmeans = KMeans(n_clusters=30, init='k-means++', max_iter=300, n_init=10, random_state=0)
colors = ['b','g','r','orange']
pred_y = kmeans.fit_predict(newData)
plt.scatter(newData[:,0], newData[:,1], s=3)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=50, c='red')
fig = plt.figure(figsize=(20,20))
plt.show()

data =DataFrame(total_num)

km = KMeans(n_clusters=20).fit(data)

cluster_map = pd.DataFrame()
cluster_map['data_index'] = data.index.values
cluster_map['cluster'] = km.labels_
cluster_map[cluster_map.cluster == 3]

all_clusters = []
for i in range(20):
    all_clusters.append(cluster_map[cluster_map.cluster == i]['data_index'].values.tolist())
all_clusters = np.array(all_clusters)

scores = []
for m in range(20):
    cluster1= []
    for i in all_clusters[m]:
        cluster1.append(total_num[i])
    c1 = DataFrame(cluster1)
    c1.columns = label
    top=[]
    for i in range(0, len(a)):
        if a[i] >1000:
            top.append(i)
    y = c1['1008']
    list1= []
    for i in top:
        if i !=8:
            list1.append(str(1000+i))
    x = c1[list1]
    x = pd.get_dummies(x)
    y = pd.get_dummies(y)

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)

    parameters = {'criterion':('gini', 'entropy'),
                  'min_samples_split':[5,6,7,8,9],
                  'max_depth':[4,5,6,7],
                  'class_weight':('balanced', None),
                  'presort':(False,True),
                 }


    tr = tree.DecisionTreeClassifier()
    gsearch = GridSearchCV(tr, parameters)
    gsearch.fit(X_train, y_train)
    model = gsearch.best_estimator_
    score = model.score(X_test, y_test)
    scores.append(score)

	dot_data = tree.export_graphviz(model, out_file=None,
	                                feature_names=X_test.columns,
	                               class_names=y_test.columns,
	                               filled=True, rounded=True,
	                               special_characters=True)
	graph = graphviz.Source(dot_data)
	filename = graph.render(filename='g%d'%m)

scores