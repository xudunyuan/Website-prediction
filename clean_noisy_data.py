import numpy as np  # linear algebra
import pandas as pd
a = []
train = pd.read_csv('trainData.csv')
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
print(new)