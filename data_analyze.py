import numpy as np  # linear algebra
import pandas as pd
import math
import datetime
import csv

def Weight(A_list, I_list, Iuf_list):
#this function takes 3 parameters: A_list and I_list are two lists containing searching history of user, Iuf_list is the list of Inverse user frenquency
#this function will return the weight between ath user and ith user.
    #print("iuf: ",Iuf_list)
    #start = datetime.datetime.now()

    U, u, u1, u2 = 0, 0, 0, 0 # U must smaller than 0
    V, v, v1, v2 = 0, 0, 0, 0 # V must smaller than 0
    B = 0
    for i in range(0, len(Iuf_list)):
        u1 = u1 + Iuf_list[i]*((A_list[i])**2)
        u2 = u2 + (Iuf_list[i]*(A_list[i]))
        v1 = v1 + Iuf_list[i]*((I_list[i])**2)
        v2 = v2 + (Iuf_list[i]*(I_list[i]))
    u = u1 - u2**2
    v = v1 - v2**2
    for i in range(0, len(Iuf_list)):
        V = V + Iuf_list[i]*v
        U = U + Iuf_list[i]*u
    B = u2*v2
    #print(U, u, u1, u2)
    #print(v1,v2)
    #print(V, v, v1, v2)

    A, a = 0, 0
    for i in range(0, len(Iuf_list)):
        a = a + Iuf_list[i] * A_list[i] * I_list[i]
    for i in range(0, len(Iuf_list)):
        A = A + Iuf_list[i] * a
    #print(A, a)
    #print(B, b1, b2)
    #print("ABUV: ",A,B,U,V)
    #print("A-B: ", A-B)
    #print("root of UV: ", (U*V)**(1/2))
    weight = (A-B)/((U*V)**(1/2))
    #print("weight: ",weight)
    #print("")
    #end = datetime.datetime.now()
    #print ("calculating weight takes time:")
    return weight

def Mean_Vote(num):
    num_df = total_num[num] # this is the Num th dataframe (Num is the user's input)
    sum_num = 0
    for i in range(0,len(num_df)):
        sum_num = sum_num + num_df[i]
    Mean_vote_of_num = float(sum_num) / float(len(num_df)) # mean vote value = sum of '1's / total attributes
    #print("mean vote of %d: %f"%(num, Mean_vote_of_num))
    return Mean_vote_of_num

def Collaborative_Filtering(Num):
    #print(total_row,total_column)
    #print(total_num)
    Num_df = total_num[Num] # this is the Num th dataframe (Num is the user's input)
    Mean_vote_of_Num = total_mean_vote[Num] # mean vote value = sum of '1's / total attributes

    sum_weight = 0
    total_weight = []
    for i in range(0, total_column-1):
        current_weight = Weight(Num_df, total_num[i], Inverse_User_Frenquency)
        total_weight.append(current_weight)
        sum_weight = sum_weight + abs(current_weight)
    #print("sum weight: ", sum_weight)
    #print("total weight: ", total_weight)
    #print("total mean vote: ", total_mean_vote)
    k = 1.0/sum_weight
    #print("k: ",k)
    #print(total_weight)

    Prob_list = [] # this list is for containing probabilities of user Num will visit all websites.
    for i in range(0, total_row-1):
        prob, p1 = 0, 0
        for j in range(0, total_column-1):
            dataframe_of_j = total_num[j]

            #print(total_weight[j] ,dataframe_of_j[i], total_mean_vote[j])

            p1 = p1 + (total_weight[j] * (float(dataframe_of_j[i]) - total_mean_vote[j]))
            #print(p1)
            #print(total_weight[j], dataframe_of_j[1], total_mean_vote[j],p1)
        prob = (p1*k) + (Mean_vote_of_Num)
        Prob_list.append(prob)
        #print(Mean_vote_of_Num)
        #print(k)
        #print(p1)
        #print(prob)
        #print("")
        #print("item: ", i, "prob: ", Prob_list)
    #print(Prob_list)
    return Prob_list

    # for j in range(0, total_column):
    #   mean_vote_of_j = Mean_Vote(j)
    #   dataframe_of_j = train.loc[j:j].values.tolist()[0]
    #   p1 = p1 + Weight(Num_df, dataframe_of_j, Inverse_User_Frenquency)
    # print("p1: ", p1)

    #Weight(Num_df,train.loc[0:0].values.tolist()[0], Inverse_User_Frenquency)
    #print(len(Num_df))
    #print(len(Inverse_User_Frenquency))
    #column = Num_df[i].value.tolist()
    #print(column)
    #print(sum_Num, len(Num_df))
    #print(Mean_vote_of_Num)
    #print(labels)
    #print(test.shape)
    #print(train.shape)

def main():
    all_prob_list = []
    for i in range(0, 10):
        temp = Collaborative_Filtering(i)
        all_prob_list.append(temp)
    #print(all_prob_list)
    with open("prediction.csv","w") as csvfile:
        for i in range(len(all_prob_list)):
            writer = csv.writer(csvfile)
            writer.writerow(all_prob_list[i])
    #print(len(all_prob_list[0]))


train = pd.read_csv('trainData.csv')
#test = pd.read_csv('trainData.csv')

labels = list(train.columns.values) #this is the first line of the csv file
total_column = train.shape[0]
total_row = train.shape[1]

total_num = [] #this 2D-array is for containing all value in the csv file
for i in range(0,total_column-1):
    num_df = train.iloc[i,:].values.tolist()
    num_df.pop(0)
    total_num.append(num_df)

Inverse_User_Frenquency = [] # a list contains all inverse user frenquency values
for i in range(1, len(labels)):
    column = train[labels[i]].tolist()
    Num_votes = 0
    for j in range(0, len(column)):
        if column[j] == 1:
            Num_votes = Num_votes + 1
    if Num_votes != 0:
        #print(i, ":", (total_column -1) / Num_votes)
        inverse_user_frequency = math.log ((total_column -1) / Num_votes)
        #here I used to use 10 as the base of log function, but there will be some bugs.
    else:
        #print(i, ":", "infinite")
        inverse_user_frequency = 1
    Inverse_User_Frenquency.append(inverse_user_frequency)
#print(Inverse_User_Frenquency)
total_mean_vote = [] # this is a list contains all users' mean votes
for i in range(0, total_column-1):
    total_mean_vote.append(Mean_Vote(i))


main()



