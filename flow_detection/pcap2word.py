import struct
import datetime
import pyshark
import csv
import os
import gc
gc.enable()
header=["id","timeStamp","src_ip","dst_ip","src_port","dst_port","data_bits"]
data_dir = 'E:/学习/DAPT/apt-master/apt-master/pcap-data/data_dir'
class gen_pcap_data(object):
    def __init__(self, file_path):
        self.file_path=file_path
        # self.cap= open(file_path, 'rb')
        self.sharkCap=pyshark.FileCapture(file_path,use_json=True, include_raw=True)
    def encode_flow(self):
        f=self.file_path
        fopen = open(data_dir + '/' + f.split('/')[-1].split('.')[0] + ".csv", 'a', newline='',
                          encoding='utf-8')
        writer = csv.DictWriter(fopen, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        writer.writeheader()  # 写入列名
        index=0
        for pkt in self.sharkCap:
            if pkt.highest_layer in ["ARP"] or "IP" not in pkt:
                index+= 1
                continue
            pkt_data={}
            pkt_data["id"]=index+1
            turple_data = self.gen_turple(pkt)
            pkt_data["src_ip"] = turple_data[0]
            pkt_data["dst_ip"] = turple_data[1]
            pkt_data["src_port"] = turple_data[2]
            pkt_data["dst_port"] = turple_data[3]
            del turple_data
            pkt_data["timeStamp"]=pkt.sniff_timestamp
            pkt_data["data_bits"]=str(pkt.get_raw_packet())
            index+=1
            writer.writerow(pkt_data)
            del pkt_data
            gc.collect()
    @staticmethod
    def gen_turple(pkt):
        src_ip=pkt.ip.src
        dst_ip=pkt.ip.dst
        src_port=0
        dst_port=0
        if "TCP" in pkt:
            src_port=pkt.tcp.srcport
            dst_port=pkt.tcp.dstport
        elif "UDP" in pkt:
            src_port = pkt.udp.srcport
            dst_port = pkt.udp.dstport
        turple = []
        turple.append(src_ip)
        turple.append(dst_ip)
        turple.append(src_port)
        turple.append(dst_port)
        return turple
    @staticmethod
    def bytes_to_hex(a):
        if a < 16:
            return "0" + hex(a)[2:]
        else:
            return hex(a)[2:]
if __name__ == '__main__':
    root_path="E:/学习/DAPT/apt-master/apt-master/pcap-data"
    # for root,dirs,files in os.walk(root_path):
    #     for f in files:
    # if (root + '/' + f) == 'E:/学习/DAPT/apt-master/apt-master/pcap-data/enp0s3-monday-pvt.pcap':
    #     continue
    file_path="E:/学习/DAPT/apt-master/apt-master/pcap-data/enp0s3-pvt-tuesday.pcap"
    # try:
    pcapData = gen_pcap_data(file_path)#root + '/' + f
    pcapData.encode_flow()
    # except Exception as e:
    #     print(e)






