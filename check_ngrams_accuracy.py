from nltk import ngrams
from collections import Counter

f = open("ngrams.txt")
allAttributes=[]
line = f.readline()
pre_grams, pre_targets = [],[]
while line:
    a = line.split(".")
    s1 = a[0]
    s2 = a[1]
    pre_grams.append(s1)
    pre_targets.append(s2.replace('\n', ''))
    line = f.readline()
#print(all_ante, all_seq)
f.close()

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

test_grams = []
test_preds = []

def test_gram():
    for i in range(len(all_users))  :
        if len(all_users[i]) > 3:
            sixgrams = ngrams(all_users[i], 3)
            l1 = list(sixgrams)
            for j in range(len(l1)-1):
                test_grams.append(l1[j])
                test_preds.append(all_users[i][3+j])

    result = Counter(test_grams)
    top = []
    times =[]
    d = dict(result)
    for i in d.keys():
        #print(i)
        top.append(i)
        times.append(d[i])
    rules = []
    for i in range(0, len(test_grams)):
        rule = []
        if test_grams[i] in top:
            rule.append(test_grams[i])
            rule.append(test_preds[i])
            rules.append(tuple(rule))
    finalrule = Counter(rules)
    topi = []
    timesi =[]
    d = dict(finalrule)
    for i in d.keys():
        #print(i)
        topi.append(i)
        timesi.append(d[i])

    cos_grams, cos_times =[] ,[]
    for i in range(len(topi)):
        if str(topi[i][0]) in pre_grams:
            cos_grams.append(topi[i])
            cos_times.append(timesi[i])

    #print(pre_grams)
    #print(cos_grams)
    success = []
    for i in range(len(pre_grams)):
        sum1 = 0
        suc = 0
        for j in range(len(cos_grams)):
            if str(cos_grams[j][0]) == pre_grams[i]:
                sum1 +=1
                if cos_grams[j][1] == pre_targets[i]:
                    suc+=1
        pr = suc/sum1
        success.append(pr)
    print(success)

test_gram()

#print(pre_grams)
#print(pre_targets)