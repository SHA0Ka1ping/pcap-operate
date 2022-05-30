# pcap-operate
python-pcap-handler

##CC

c&c服务器代码，可以实现命令回传，并监听连入受害者

##geo_util

根据ip查询地理位置

##model_predict

###loadModel.py
实现加载对应模型并检测目标数据文件夹中数据文件，并生成检测报告输入参数：模型路径，待检测文件路径（绝对路径）
###read_data.py
实现加载数据并转换时间戳，用于训练模型的类get_data
####gen_total_data
这个方法实现了扫描文件中所有csv数据并将之提取到一个csv中
####gen_data_label
这个方法实现了提取用于训练的数据特征与对应标签，返回对应的dataframe对象
####num_labels
这个方法将字符形标签转化为数字

'Benign':0

'Lateral Movement':1

'Reconnaissance':3

'Establish Foothold':4

'Data Exfiltration':5
####时间戳转换方法
composeTime:实现将"%Y_%m_%d %H:%M:%S"时间戳转换为微秒

seconds2timeStam:与以上方法相反
###retrain.py
这个模块实现了根据已有数据重新训练模型，输入参数为：数据文件夹绝对路径，模型保存路径



