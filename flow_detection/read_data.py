import pandas as pd
import os
import time
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
path='E:/学习/flow_detection/data/csv'
def trans_timestamp(timestamp):
    #15/07/2019 01:55:22 PM
    #transfer to second(1970)
    dates="".join(timestamp[:10])
    times="".join(timestamp[11:19])
    hours="".join(timestamp[-2:])
    date=dates.split('/')
    timess=times.split(':')
    for i in range(3):
        date[i]=int(date[i])
        timess[i]=int(timess[i])
    if hours=='PM':
        timess[0]+=12
        if timess[0]==24:
            timess[0]=0
    newStamp="{:d}_{:d}_{:d} {:d}:{:d}:{:d}".format(date[2],date[1],date[0],timess[0],timess[1],timess[2])
    def composeTime(time1):
        time2 = datetime.datetime.strptime(time1, "%Y_%m_%d %H:%M:%S")
        time3 = time.mktime(time2.timetuple())
        time4 = int(time3)
        return time4
    return composeTime(newStamp)
def gen_total_data():
    data=pd.DataFrame()
    for root,dirs,files in os.walk(path):
        for file in files:
            data=pd.concat([data,pd.read_csv(root+'/'+file)])
    data.to_csv(root+'/'+'total_data.csv')
    print(data.head())
def gen_data_label():
    data=pd.read_csv(path+'/total_data.csv')
    # fig=plt.figure(figsize=(14.4,6.4))
    # ax=sns.countplot(x="Stage", data=data)
    # plt.show()
    use_data=data.drop(["Flow ID","Src IP","Src Port","Dst IP","Dst Port","Activity","Stage"],axis=1)
    for index,row in use_data.iterrows():#row为迭代器
        timestamp=row["Timestamp"]
        use_data.loc[index,"Timestamp"]=trans_timestamp(timestamp)
    label_data=data.loc[:,"Stage"] #第一个引号是行的范围，第二个引号是列的范围"Activity":"Stage"
    base_info=use_data.iloc[:,0:6]
    # print(label_data.head(),type(data["Stage"]))
    # print(use_data.head())
    return use_data,label_data,base_info
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
if __name__ == '__main__':
    #gen_total_data()
    num_labels(gen_data_label()[1])