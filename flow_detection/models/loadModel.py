import pickle as pk
import pandas as pd
import read_data as rd
import csv
import sys
class loadModel(object):
    def __init__(self,model_file,data_file,data_dir):
        self.model_file=model_file
        self.data_file=data_file
        self.data_dir=data_dir
    def load_model(self):
        with open(self.model_file,'rb') as f:
            m=pk.load(f)
        return m
    def load_data(self):
        data = pd.read_csv(self.data_dir+'/'+self.data_file)
        use_data = data.drop(["Flow ID", "Src IP", "Src Port", "Dst IP", "Dst Port", "Activity", "Stage"], axis=1)
        for index, row in use_data.iterrows():  # row为迭代器
            timestamp = row["Timestamp"]
            use_data.loc[index, "Timestamp"] = rd.trans_timestamp(timestamp)
        base_info = use_data.iloc[:, 0:6]
        return use_data,base_info
    def predict(self,m,data):
        data_predict=m.predict(data)
        res=[]
        for d in data_predict:
            if d==0.0:
                res.append('Benign')
            elif d==1.0:
                res.append('Lateral Movement')
            elif d==3.0:
                res.append('Reconnaissance')
            elif d==4.0:
                res.append('Establish Foothold')
            elif d==5.0:
                res.append('Data Exfiltration')
        res=pd.Series(res)
        return res
    def gen_results(self,data,result):
        file=self.data_file.split('.')[0]+'-result'+'.csv'
        target_path=self.data_dir+'/'+file
        data["Activity"]=result
        data["Stage"]=result
        data.to_csv(target_path)
