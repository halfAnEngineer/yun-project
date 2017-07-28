# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 20:06:48 2017
@author: liyun
"""


#==============================================================================
# #提取出来原始文件中 6点~9点 的所有数据，并存入 yun_data_6_9
# data=[]
# with open('gy_contest_link_traveltime_training_data.txt') as f:
#     print(f.readline())
#     while True:
#         line=f.readline()
#         if not line:
#             break
#         if int(line[43:45])>=6 and int(line[43:45])<9:
#             data.append(line)
# with open('yun_data_6_9.txt','w',newline='') as f:
#     f.writelines(data)
#==============================================================================


#==============================================================================
#提取出来 yun_data_6_9 中的所有数据, 6点~8点 的数据存入 yun_data_6_8 , 8点~9点 的数据存入 yun_data_8_9
#data1=[]
#data2=[]
#with open('yun_data_6_9.txt') as f:
#    while True:
#        line=f.readline()
#        if not line:
#            break
#        if int(line[43:45])>=6 and int(line[43:45])<8:
#            data1.append(line)
#        else:
#            data2.append(line)
#with open('yun_data_6_8.txt','w',newline='') as f:
#    f.writelines(data1)
#with open('yun_data_8_9.txt','w',newline='') as f:
#    f.writelines(data2)
#==============================================================================


#把 3月~5月 8点~9点 的历史数据提取出来，相同的 (link,星期几,时间片) 求和，平均，作为 6月 8点~9点 的预测值
first_day=(2,5,7,3) # 3月~6月 的第一天是星期几
data=[]
Dict={} # 从 (link,星期几,时间片) 到 [加和，数量] 的映射
Link=set()
with open('yun_data_8_9.txt') as f:
    while True:
        line=f.readline()
        if not line:
            break
        line=line[:-1]
        line=line.split(';')
        weekday=(int(line[1][8:10])+first_day[int(line[1][5:7])-3]-2)%7+1
        times=int(line[2][15:17])
        x=(line[0],weekday,times)
        Link.add(line[0])
        if x in Dict:
#            Dict[x][0]+=float(line[3])
#            Dict[x][1]+=1
            Dict[x].append(float(line[3]))
        else:
            Dict[x]=[float(line[3])]
Link=list(Link)

#将 Dict 中缺失的东西补齐，并求出预测值放入 Dict2 ,有多个值求中位数，没有值就等于前面那个数的值
Dict2={}
prevalue=5.0
for link in Link:
    for day in range(7):
        for minute in range(30):
            x=(link,day+1,minute*2);
            if x in Dict:
                y=sorted(Dict[x])
                z=max(int(len(y)/2)-1,0)
                
                Dict2[x]=y[z]
                prevalue=y[z]
            else:
                Dict2[x]=prevalue;


#将结果保存为 .txt 文件
filename='yun_20170725.txt'         
knt=0
with open(filename,'w') as f:
    for link in Link:
        for day in range(30):
            for minute in range(30):
                
                if knt==0:
                    knt+=1
                    temp=''
                else:
                    temp='\n'
                
                temp+=link+'#'
                if day<9:
                    date='2016-06-0'+str(day+1)
                else:
                    date='2016-06-'+str(day+1)
                temp+=date+'#['+date+' 08:'
                if minute<5:
                    temp+='0'+str(minute*2)+':00,'+date+' 0'
                else:
                    temp+=str(minute*2)+':00,'+date+' 0'
                if minute==29:
                    temp+='9:00:00)#'
                else:
                    temp+='8:'
                    if minute<4:
                        temp+='0'+str(minute*2+2)+':00)#'
                    else:
                        temp+=str(minute*2+2)+':00)#'
                
                x=(link,(day-1+first_day[3])%7+1,minute*2)
                temp+=str(Dict2[x])
                
                f.write(temp)
                
























































































