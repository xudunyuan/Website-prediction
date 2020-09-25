import csv
f = open("train_data.txt")
allAttributes=[]
line = f.readline()
while line:
    a = line.split(",")
    if len(a) >= 2:
        if a[0] == "A":
            allAttributes.append(a[1])
    line = f.readline()
f.close()


for i in range(0, len(allAttributes)):
    for j in range(i , len(allAttributes)):
        if allAttributes[i] > allAttributes[j]:
            temp = allAttributes[j]
            allAttributes[j] = allAttributes[i]
            allAttributes[i] = temp

# for i in range(len(allAttributes)):
#     print(allAttributes[i])

allAttributes.insert(0," ")

with open("trainData.csv","w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(allAttributes)

instance = []
f = open("train_data.txt")
line = f.readline()
while line:
    a = line.split(",")
    if len(a) >= 2:
        if a[0] == "C":
            #writer.writerow(instance)
            instance = []
            instance.append(a[1])
            line = f.readline()
            a = line.split(",")
            while a[0] == "V":
                instance.append(a[1])
                line = f.readline()
                a = line.split(",")
            print(instance)
            row = []
            for i in range(len(allAttributes)):
                row.append(0)
            for k in range(1, len(instance)):
                for j in range(len(allAttributes)):
                    if instance[k] == allAttributes[j]:
                        row[j-1] = 1
                        break
            row.insert(0, instance[0])
            with open("trainData.csv","a+") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(row)
        else:
            line = f.readline()
f.close()
#



