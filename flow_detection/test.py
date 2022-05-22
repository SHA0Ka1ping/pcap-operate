import pyshark
file_path="E:/学习/DAPT/apt-master/apt-master/pcap-data/enp0s3-pvt-tuesday.pcap"
cap=pyshark.FileCapture(file_path,use_json=True, include_raw=True)
for packet in cap:
    print(str(packet.get_raw_packet()))
    break

# string_data=self.cap.read()
        # packet_num=0
        # # packet_data = []
        # # packet_time = []
        # i = 24
        # f=self.file_path
        # fopen=open(data_dir + '/' + f.split('/')[-1].split('.')[0] + ".csv", 'a', newline='',
        #           encoding='utf-8')
        # writer = csv.DictWriter(fopen, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        # writer.writeheader()  # 写入列名
        # fopen.close()
        # while (i < len(string_data)):
        #     packet_time = string_data[i:i + 4]
        #     packet_len = struct.unpack('I', string_data[i + 12:i + 16])[0]
        #     packet_data = string_data[i + 16:i + 16 + packet_len]
        #     i = i + packet_len + 16
        #     if self.sharkCap[packet_num].highest_layer in ["ARP"] or "IP" not in self.sharkCap[packet_num]:
        #         packet_num += 1
        #         continue
        #     packet_dict = {}
        #     id = str(packet_num + 1)
        #     timeStamp = int(str(hex(packet_time[3])[
        #                         2:] + hex(packet_time[2])[2:] + hex(packet_time[1])[2:] + hex(packet_time[0])[
        #                                                                                   2:]), 16)
        #     del packet_time
        #     dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
        #     otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        #     data_bits = ""
        #     for j in range(0, len(packet_data)):
        #         data_bits += self.bytes_to_hex(packet_data[j]) + " "
        #     del packet_data
        #     packet_dict["id"] = id
        #     del id
        #     packet_dict["timeStamp"] = otherStyleTime
        #     del otherStyleTime
        #     packet_dict["data_bits"] = data_bits
        #     del data_bits
        #     print(packet_num, self.sharkCap[packet_num])
        #     turple_data = self.gen_turple(self.sharkCap[packet_num])
        #     packet_dict["src_ip"] = turple_data[0]
        #     packet_dict["dst_ip"] = turple_data[1]
        #     packet_dict["src_port"] = turple_data[2]
        #     packet_dict["dst_port"] = turple_data[3]
        #     del turple_data
        #     gc.collect()
        #     packet_num += 1
        #     fopen = open(data_dir + '/' + f.split('/')[-1].split('.')[0] + ".csv", 'a', newline='',
        #                  encoding='utf-8')
        #     writer = csv.DictWriter(fopen, fieldnames=header)
        #     writer.writerow(packet_dict)
        #     fopen.close()
        # self.cap.close()