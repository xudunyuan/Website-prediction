from numpy import *

#read txt file to get the dataset
def loadDataSet():
    f = open("train_data.txt")
    dataset = []
    line = f.readline()
    while line:
        a = line.split(",")
        if len(a) >= 2:
            if a[0] == "C":
                instance = []
                line = f.readline()
                a = line.split(",")
                while a[0] == "V":
                    instance.append(a[1])
                    line = f.readline()
                    a = line.split(",")
                dataset.append(instance)
            else:
                line = f.readline()
    return dataset

#generate C1 table
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))


#generate a dictionary contains all frenquency items and their supports
def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not can in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
            supportData[key] = support
    return retList, supportData


def calSupport(D, Ck, min_support):
    dict_sup = {}  # this is a dictionary contains all items and how many times they appear
    for i in D:
        for j in Ck:
            if j.issubset(i):
                if not j in dict_sup:
                    dict_sup[j] = 1
                else:
                    dict_sup[j] += 1
    sumCount = float(len(D)) # the total number of itemsets
    supportData = {} # this is a dictionary contains all items meet the requirement and their support value
    relist = [] # this is a list contains all items meet the requirement
    for i in dict_sup:
        temp_sup = dict_sup[i] / sumCount
        if temp_sup >= min_support:
            relist.append(i)
            supportData[i] = temp_sup
    #print(relist, supportData)
    return relist, supportData


def aprioriGen(Lk, k):  # 创建候选K项集 ##LK为频繁K项集
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:  # if the two itemsets' first n-1 items are the same, we combine them together
                a = Lk[i] | Lk[j]  # a is the combination of these two itemsets
                a1 = list(a)
                b = [] # b is a list contains all subsets of a
                for q in range(len(a1)):
                    t = [a1[q]]
                    tt = frozenset(set(a1) - set(t))
                    b.append(tt)
                t = 0
                #test how many elements in a is contained in Lk (origina dataset)
                for w in b:
                    if w in Lk:
                        t += 1
                # if all elements in b is contained in Lk, which means all subsets of a is subsets of Lk, then a is an acceptable combination.
                if t == len(b):
                    retList.append(a)
    return retList


def apriori(dataSet, minSupport=0.2):
    C1 = createC1(dataSet)
    D = list(map(set, dataSet))
    L1, supportData = calSupport(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k - 2]) > 0):
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minSupport)  # scan DB to get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    del L[-1]
    return L, supportData  #L is the frenquency set, it's a list


# generate all subsets
def getSubset(fromList, toList):
    for i in range(len(fromList)):
        t = [fromList[i]]
        tt = frozenset(set(fromList) - set(t))
        if not tt in toList:
            toList.append(tt)
            tt = list(tt)
            if len(tt) > 1:
                getSubset(tt, toList)


def calcConf(freqSet, H, supportData, ruleList, minConf=0.7, minlift = 1):
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]  # calculate confidence
        # 提升度lift计算lift = p(a & b) / p(a)*p(b)
        lift = supportData[freqSet] / (supportData[conseq] * supportData[freqSet - conseq])

        if conf >= minConf and lift > minlift:
            f = open('rules.txt','a')
            set_freqSet = set(freqSet - conseq)
            set_conseq = set(conseq)
            s1, s2 = "", ""
            for i in (set_freqSet):
                s1 = s1 + str(i) + str(" ")
            for i in (set_conseq):
                s2 = s2 + str(i) + str(" ")
            f.write(str(s1+ "."+ s2))
            f.write('\n')
            f.close()
            print("rule ", len(ruleList), ":  ", set(freqSet - conseq), '-->', set(conseq), 'support: ', round(supportData[freqSet - conseq], 2), 'confidence: ', conf,
                  'lift value：', round(lift, 2))
            ruleList.append((freqSet - conseq, conseq, conf))

# generate rules
def gen_rule(L, supportData, minConf=0.7, minlift = 1):
    bigRuleList = []
    for i in range(1, len(L)):  # 从二项集开始计算
        for freqSet in L[i]:  # freqSet为所有的k项集
            # 求该三项集的所有非空子集，1项集，2项集，直到k-1项集，用H1表示，为list类型,里面为frozenset类型，
            H1 = list(freqSet)
            all_subset = []
            getSubset(H1, all_subset)  # 生成所有的子集
            calcConf(freqSet, all_subset, supportData, bigRuleList, minConf, minlift)
    return bigRuleList


if __name__ == '__main__':
    dataSet = loadDataSet()
    L, supportData = apriori(dataSet, minSupport = 0.01)
    rule = gen_rule(L, supportData, minConf=0.8, minlift = 5)