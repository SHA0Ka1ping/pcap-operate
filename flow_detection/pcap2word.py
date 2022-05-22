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
        self.cap= open(file_path, 'rb')
        self.sharkCap=pyshark.FileCapture(file_path)
    def encode_flow(self):
        string_data=self.cap.read()
        packet_num=0
        # packet_data = []
        # packet_time = []
        i = 24
        f=self.file_path
        with open(data_dir + '/' + f.split('/')[-1].split('.')[0] + ".csv", 'a', newline='',
                  encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
            # writer.writeheader()  # 写入列名
            while (i < len(string_data)):
                packet_time=string_data[i:i + 4]
                packet_len = struct.unpack('I', string_data[i + 12:i + 16])[0]
                packet_data=string_data[i + 16:i + 16 + packet_len]
                i = i + packet_len + 16
                if self.sharkCap[packet_num].highest_layer in ["ARP"] or "IP" not in self.sharkCap[packet_num]:
                    packet_num+=1
                    continue
                packet_dict={}
                id=str(packet_num + 1)
                timeStamp = int(str(hex(packet_time[3])[
                                    2:] + hex(packet_time[2])[2:] + hex(packet_time[1])[2:] + hex(packet_time[0])[
                                                                                                    2:]), 16)
                del packet_time
                dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
                otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
                data_bits=""
                for j in range(0, len(packet_data)):
                    data_bits+= self.bytes_to_hex(packet_data[j]) + " "
                del packet_data
                packet_dict["id"]=id
                del id
                packet_dict["timeStamp"]=otherStyleTime
                del otherStyleTime
                packet_dict["data_bits"]=data_bits
                del data_bits
                print(i,self.sharkCap[packet_num])
                turple_data=self.gen_turple(self.sharkCap[packet_num])
                packet_dict["src_ip"]=turple_data[0]
                packet_dict["dst_ip"] = turple_data[1]
                packet_dict["src_port"] = turple_data[2]
                packet_dict["dst_port"] = turple_data[3]
                del turple_data
                writer.writerow(packet_dict)
                gc.collect()
                packet_num += 1
        self.cap.close()
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






