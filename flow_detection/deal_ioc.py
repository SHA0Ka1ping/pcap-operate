from collections import defaultdict
ioc_base=defaultdict(list)
f=open('iocs.txt','r',encoding='utf-8')
i=0
type=''
for line in f.readlines():
    if i%2==0:
        type=line.replace('\n','')
        i+=1
    else:
        ioc_base[type].append(line.replace('\n',''))
        i+=1
path=r'E:/学习/flow_detection/ioc_base/'
for k in ioc_base.keys():
    with open(path+k+'.txt','a',newline='',encoding='utf-8') as f:
        for l in ioc_base[k]:
            f.write(l+'\n')
        f.close()
