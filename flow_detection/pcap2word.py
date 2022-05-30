import struct
import datetime
import pyshark
import csv
import os
import gc
import getUrl
from scapy.all import *
gc.enable()
header=["flow_id","timeStamp","src_ip","dst_ip","src_port","dst_port","data_bits","url"]
data_dir = r'E:\学习\DAPT\apt-master\apt-master\pcap-data\newDatas'
def save2file(f, pkt_data, isHeaderWritted=False):
    fopen = open(data_dir + '/' + f.split('/')[-1].split('.')[0] + ".csv", 'a', newline='',
                 encoding='utf-8')
    print(1)
    writer = csv.DictWriter(fopen, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
    if not isHeaderWritted:
        writer.writeheader()  # 写入列名
    writer.writerow(pkt_data)
    fopen.close()
class gen_pcap_data(object):
    def __init__(self, file_path):
        self.file_path=file_path
        # self.cap= open(file_path, 'rb')
        # self.sharkCap=pyshark.FileCapture(file_path,use_json=True, include_raw=True)
        self.pr =  PcapReader(file_path)
    def encode_flow(self):
        fopen = open(data_dir + '/' + self.file_path.split('/')[-1].split('.')[0] + ".csv", 'w', newline='',encoding='utf-8')
        writer = csv.DictWriter(fopen, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        writer.writeheader()  # 写入列名
        index=0
        # print(repr(self.pr.read_packet()))
        while True:
            try:
                pkt = self.pr.read_packet()
            except:
                pkt=None
            print(repr(pkt))
            if pkt is None:
                break
            pkt_data = {}
            pkt_data["flow_id"] = index + 1
            turple_data = self.gen_turple(pkt)
            if turple_data == False:
                index += 1
                continue
            pkt_data["src_ip"] = turple_data[0]
            pkt_data["dst_ip"] = turple_data[1]
            pkt_data["src_port"] = turple_data[2]
            pkt_data["dst_port"] = turple_data[3]
            pkt_data["timeStamp"] = pkt.time
            try:
                if "Raw" in pkt:
                    pkt_data["data_bits"] = pkt["Raw"].load #.decode('utf-8')
                    pkt_data["url"] = getUrl.retUrl(pkt)
                else:
                    pkt_data["data_bits"] = ""
                    pkt_data["url"] = ""
            except:
                if "Raw" in pkt:
                    pkt_data["data_bits"] = pkt["Raw"].load
                    pkt_data["url"] = ""
                else:
                    pkt_data["data_bits"] = ""
                    pkt_data["url"] = ""
            index += 1
            print(index)
            writer.writerow(pkt_data)
            # save2file(self.file_path, pkt_data, index == 0)
            # print(pkt_data)
            # del pkt_data
            gc.collect()

        print("done!")
    @staticmethod
    def gen_turple(pkt):
        src_port=''
        dst_port=''
        if "IP" in pkt:
            src_ip = pkt["IP"].src
            dst_ip = pkt["IP"].dst
        else:
            return False
        if "TCP" in pkt:
            src_port = pkt["TCP"].sport
            dst_port = pkt["TCP"].dport
        if "UDP" in pkt:
            src_port = pkt["UDP"].sport
            dst_port = pkt["UDP"].dport
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
    file_path="E:/学习/DAPT/apt-master/apt-master/pcap-data/enp0s3-monday-pvt.pcap"
    # try:
    pcapData = gen_pcap_data(file_path)#root + '/' + f
    pcapData.encode_flow()
    # except Exception as e:
    #     print(e)






