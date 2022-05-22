import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
path='E:/学习/tf-learning/data/csv'
def gen_total_data():
    data=pd.DataFrame()
    for root,dirs,files in os.walk(path):
        for file in files:
            data=pd.concat([data,pd.read_csv(root+'/'+file)])
    #data.to_csv(root+'/'+'total_data.csv')
    print(data.head())
def gen_data_label():
    data=pd.read_csv(path+'/total_data.csv')
    # fig=plt.figure(figsize=(14.4,6.4))
    # ax=sns.countplot(x="Stage", data=data)
    # plt.show()
    use_data=data.drop(["ID","Flow ID","Src IP","Src Port","Dst IP","Dst Port","Src IP","Timestamp","Activity","Stage"],axis=1)
    label_data=data.loc[:,"Stage"] #第一个引号是行的范围，第二个引号是列的范围"Activity":"Stage"
    # print(label_data.head(),type(data["Stage"]))
    # print(use_data.head())
    return use_data,label_data
def num_labels(label_data):
    label_list=label_data.values.tolist();
    cnt=Counter(label_list)
    keys=[]
    for k in cnt.keys():
        keys.append(k)
    numLabels=[]
    for lb in label_list:
        if lb==keys[0] or lb==keys[2]:
            numLabels.append(0)
        elif lb==keys[1]:
            numLabels.append(1)
        elif lb==keys[3]:
            numLabels.append(3)
        elif lb==keys[4]:
            numLabels.append(4)
        elif lb==keys[5]:
            numLabels.append(5)
    numLabels=pd.Series(numLabels) #{"Stage":numLabels}
    # print(numLabels.head(),type(numLabels))
    return numLabels
num_labels(gen_data_label()[1])