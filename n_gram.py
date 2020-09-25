from nltk import ngrams
from collections import Counter

f = open("train_data.txt")

#get all websites
allAttributes=[]
line = f.readline()
while line:
    a = line.split(",")
    if len(a) >= 2:
        if a[0] == "A":
            allAttributes.append(a[1])
    line = f.readline()
f.close()

#sort
for i in range(0, len(allAttributes)):
    for j in range(i , len(allAttributes)):
        if allAttributes[i] > allAttributes[j]:
            temp = allAttributes[j]
            allAttributes[j] = allAttributes[i]
            allAttributes[i] = temp

f = open("train_data.txt")
all_users = []
line = f.readline()
while line:
    a = line.split(",")
    if len(a) >= 2:
        instance = []
        if a[0] == "C":
            #writer.writerow(instance)
            #instance.append(a[1])
            line = f.readline()
            a = line.split(",")
            while a[0] == "V":
                instance.append(a[1])
                line = f.readline()
                a = line.split(",")
            #print(instance)
        else:
            line = f.readline()
        all_users.append(instance)
f.close()

all_grams = []
all_preds = []


def n_gram(grams, rules_num, preds_num, min_prob):
    for i in range(len(all_users))  :
        if len(all_users[i]) > grams:
            sixgrams = ngrams(all_users[i], grams)
            l1 = list(sixgrams)
            for j in range(len(l1)-1):
                all_grams.append(l1[j])
                all_preds.append(all_users[i][grams+j])

    result = Counter(all_grams)
    top = []
    times =[]
    d = dict(result)
    for i in d.keys():
        if d[i] >= rules_num:
            #print(i)
            top.append(i)
            times.append(d[i])
    rules = []
    for i in range(0, len(all_grams)):
        rule = []
        if all_grams[i] in top:
            rule.append(all_grams[i])
            rule.append('-->')
            rule.append(all_preds[i])
            rules.append(tuple(rule))
    finalrule = Counter(rules)
    topi = []
    timesi =[]
    d = dict(finalrule)
    for i in d.keys():
        if d[i] >= preds_num:
            #print(i)
            topi.append(i)
            timesi.append(d[i])
    probs = []
    for i in range(len(topi)):
        for j in range(len(top)):
            if top[j] == topi[i][0]:
                #print(j,i)
                prob = timesi[i] / times[j]
                #print(prob)
                probs.append(prob)
    for i in range(len(topi)):
    	if probs[i] >= min_prob:
        	print("rules: ",topi[i], ". prob:", probs[i])

    f = open('ngrams.txt','a')
    for i in range(len(topi)):
    	if probs[i] >= min_prob:
	    	s1, s2 = "", ""
	    	for j in range(len(topi[i])-2):
	    		s1 = s1 + str(topi[i][j])
	    	s2 = str(topi[i][len(topi[i])-1])
	    	f.write(str(s1+ "."+ s2))
	    	f.write('\n')
    f.close()

n_gram(3, 100, 10, 0.3)
