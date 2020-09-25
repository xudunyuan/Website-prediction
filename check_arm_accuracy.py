import numpy as np  # linear algebra
import pandas as pd
f = open("rules.txt")
allAttributes=[]
line = f.readline()
all_ante, all_seq = [],[]
while line:
    ante, seq = [],[]
    a = line.split(".")
    s, s1 = "", ""
    i, j = 0, 0
    while i < len(list(a[0])):
        while list(a[0])[i] != ' ':
            s = s + str(list(a[0])[i])
            i+=1
        ante.append(s)
        s = ""
        i+=1

    while j < len(list(a[1]))-1:
        while list(a[1])[j] != ' ' and j < len(list(a[1])):
            s1 = s1 + str(list(a[1])[j])
            j+=1
        seq.append(s1)
        s1 = ""
        j+=1
    all_seq.append(seq)
    all_ante.append(ante)
    line = f.readline()
#print(all_ante, all_seq)
f.close()


train = pd.read_csv('testData.csv')
#test = pd.read_csv('trainData.csv')

labels = list(train.columns.values) #this is the first line of the csv file
total_column = train.shape[0]
total_row = train.shape[1]

total_rate = []
for j in range(len(all_ante)):
    #print(i)
    #print(column)
    success, total = 0, 0
    for i in range(0, total_column-1):
        column = train.iloc[i,:].values.tolist()
        satisfy = True
        for k in all_ante[j]:
            if column[int(k) - 999] == 0:
                satisfy = False
        if satisfy == True:
            #print(i, j)
            total +=1
            if column[int(all_seq[j][0]) - 999] == 1:
                success += 1
    if total != 0:
        total_rate.append(float(success)/total)
print("success rate: ", total_rate)
#print(success, total)