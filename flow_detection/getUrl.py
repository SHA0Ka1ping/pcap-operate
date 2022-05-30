
from scapy.all import *

dataDir="E:/学习/DAPT/apt-master/apt-master/pcap-data/urlBase/"

def retUrl(pkt):
    text = pkt["Raw"].load.decode('utf-8')
    if "GET " == text[:4] or "POST " == text[:5]:
        info = text.split("\r\n")
        uri = info[0].split(" ")[1]
        # 此处获取到的是所有的参数，不过目前我们只提取了host字段而已
        other_info_dict = dict((x.split(":")[0], x.split(":")[1]) for x in info[1:] if ":" in x)
        host = ""
        if "Host" in other_info_dict:
            host = other_info_dict["Host"]
        return host + uri
    return ''
class gen_urls(object):
    def __init__(self,data_dir):
        self.data_dir=data_dir
    def getUrls(self,file_name):
        with open(dataDir+file_name.split('/')[-1].split('.')[0]+'.txt','a',newline='',
                       encoding='utf-8') as f:
            pr = PcapReader(file_name)
            # 逐包读取
            while True:
                # 有的数据，没有实际数据层，所以这里排除掉那类错误
                try:
                    package = pr.read_packet()
                    if package is None:
                        break
                    text = package["Raw"].load.decode('utf-8')
                    if "GET " == text[:4] or "POST "==text[:5]:
                        info = text.split("\r\n")
                        uri = info[0].split(" ")[1]
                        # 此处获取到的是所有的参数，不过目前我们只提取了host字段而已
                        other_info_dict = dict((x.split(":")[0], x.split(":")[1]) for x in info[1:] if ":" in x)
                        host = ""
                        if "Host" in other_info_dict:
                            host = other_info_dict["Host"]
                        print(host + uri)
                        f.write(host+uri+"\n")
                except:
                    pass
            print("done!")
            f.close()
if __name__ == '__main__':
    gurls=gen_urls(dataDir)
    gurls.getUrls("E:/学习/DAPT/apt-master/apt-master/pcap-data/enp0s3-monday-pvt.pcap")