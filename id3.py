from sklearn.model_selection import train_test_split
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import cross_val_score
from sklearn import tree
from sklearn.model_selection import GridSearchCV
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import graphviz

# load the data
df = pd.read_csv('/Users/xudunyuan/Desktop/data mining individual/web/trainData.csv')
# split the data int x(training data) and y (results)
y = df['1008']
list1= ['1000', '1001', '1002', '1003', '1004', '1009']
x = df[list1]
x = pd.get_dummies(x)
y = pd.get_dummies(y)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)

parameters = {'criterion':('gini', 'entropy'),
              'min_samples_split':[2,3,4,5],
              'max_depth':[9,10,11,12],
              'class_weight':('balanced', None),
              'presort':(False,True),
             }


tr = tree.DecisionTreeClassifier()
gsearch = GridSearchCV(tr, parameters)
gsearch.fit(X_train, y_train)
model = gsearch.best_estimator_

score = model.score(X_test, y_test)
print(score)

dot_data = tree.export_graphviz(model, out_file=None,
                                feature_names=X_test.columns,
                               class_names=y_test.columns,
                               filled=True, rounded=True,
                               special_characters=True)
graph = graphviz.Source(dot_data)
filename = graph.render(filename='g1')
print(filename)
# gsearch.cv_results_