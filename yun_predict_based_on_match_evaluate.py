# -*- coding: utf-8 -*-
# @Time    : 2017/7/27 19:55
# @Author  : LiYun
# @File    : predict_based_on_match.py
'''description:
线下评估及调参，5月1号至5月30号 8:00至9:00 作为预测值
基于匹配的预测
'''

import numpy as np
import matplotlib.pyplot as plt
import yun_estimate_result

# 每个月有几天,没有考虑闰年
mdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# 输入数据中每行元素的起始位置，分别为
# link的结束位置，月，日，（起始时，分，秒），（终止时，分，秒），通行时间
Lp = [19, 25, 28, 43, 46, 49, 63, 66, 69, 73]

def readdata(infile):
    '''从输入文件中读取数据，将数据存储在列表里并返回，注意输入文件没有表头'''
    data = []
    with open(infile) as f:
        while True:
            line = f.readline()
            if not line:
                break
            data.append(line[:-1])
    return data

def get_all_links(linkinfo):
    '''给定link信息文件，返回所有路段的名称与对应序号所构成的字典'''
    Links=[]
    with open(linkinfo) as f:
        f.readline()
        while True:
            line=f.readline()
            if not line:
                break
            Links.append(line[:Lp[0]])
    Links=sorted(Links)
    Links2={}
    Links3={}
    num=0
    for l in Links:
        Links2[l]=num
        Links3[num]=l
        num+=1
    return Links2,Links3

def get_day(d,btime):
    '''给定日期，推出这是第几天，从3月1日开始算起'''
    if d[:2]==btime[:2]: #相同月份
        return int(d[3:5])-int(btime[3:5])
    else: #不同月份
        a=int(btime[3:5])
        b=int(d[3:5])
        for i in range(int(btime[:2]),int(d[:2])):
            b+=mdays[i-1]
        return b-a

def get_slide(t):
    '''给定时间，推出这是第几个时间片'''
    bm=int(t[:2])*60+int(t[3:5])
    em=int(t[6:8])*60+int(t[9:])
    return int((em-bm)/2)

def get_history(data,Links):
    '''得到3 月至4 月每天 01:00 到 23:00 的历史数据
    和5月每天 07:00 到 08:00 的当前数据'''
    his=np.empty((61,660,132),np.float) #一共是92天，22个小时是22*30=660个时间片，一共132条Link
    cur=np.empty((30,30,132),np.float) #一共是30天，30个时间片，一共132条Link
    for info in data:
        if int(info[Lp[1]:Lp[1]+2])==6:
            continue
        elif int(info[Lp[1]:Lp[1]+2])==5:
            if int(info[Lp[3]:Lp[3] + 2]) < 7 or int(info[Lp[3]:Lp[3] + 2]) >= 8 or int(info[Lp[2]:Lp[2] + 2]) ==31:
                # 不使用07:00 到 8:00以外的数据 和5月31号的数据
                continue
            link_id=Links[info[:Lp[0]]] #路段对应的标号
            day=get_day(info[Lp[1]:Lp[1]+5],'05-01') #第几天，从'05-01'算起
            slide=get_slide('07:00-'+info[Lp[3]:Lp[3]+5]) #第几个时间片，从'07:00'算起
            cur[day,slide,link_id]=float(info[Lp[9]:])
        elif int(info[Lp[3]:Lp[3]+2])<1 or int(info[Lp[3]:Lp[3]+2])>=23:
            # 不使用01:00 到 23:00以外的数据
            continue
        else:
            link_id=Links[info[:Lp[0]]] #路段对应的标号
            day=get_day(info[Lp[1]:Lp[1]+5],'03-01') #第几天，从'03-01'算起
            slide=get_slide('01:00-'+info[Lp[3]:Lp[3]+5]) #第几个时间片，从'01:00'算起
            his[day,slide,link_id]=float(info[Lp[9]:])
    return his,cur

#将历史数据和当前数据提取并保存
# data=readdata('yun_complement_dataset.txt') #假设历史数据集是完备的
Links,Links2=get_all_links('gy_contest_link_info.txt') #所有路段的名称与对应序号所构成的字典，序号与路段构成的字典
#历史数据，3月至5月，一共是92天，660个时间片，132条Link，92*660*132
#当前数据，6月份，7:00-8:00的数据，一共是30天，30个时间片，132条Link，30*30*132
# his,cur=get_history(data,Links)
# np.savez('yun_match_data_evaluate',his,cur)

#读取历史数据和当前数据
temp=np.load('yun_match_data_evaluate.npz')
his,cur=temp['arr_0'],temp['arr_1']

#找到每一天最匹配的数据作为预测值
prediction=np.empty((30,30,132),np.float) #预测值，5月份，8:00-9:00的数据，一共是30天，30个时间片，132条Link，30*30*132
for day in range(30):
    cur_data=np.hstack(cur[day])
    min_value=np.empty((61,3),np.float) #记录天数，每天最匹配的slide的位置和匹配程度(越小越好)
    for day2 in range(61):
        knt_min=np.array([day2,0,1e8])
        for slide in range(601): #660-30-30 最后30个时间片不能用，作为预测值保留，每个向量是30个时间片，一共可以形成151个向量
            if slide==0:
                his_data=np.hstack(his[day2,:30])
            else:
                his_data=np.hstack((his_data[132:],his[day2,slide+29])) #去掉最前面一个时间片的信息，加入下一个时间片的信息
            dis=np.sum(np.abs(cur_data - his_data)/cur_data) #计算两个向量的距离
            # print(dis)
            if dis<knt_min[2]:
                knt_min[1]=slide+30 #直接记录作为预测值的起始位置
                knt_min[2]=dis
        min_value[day2]=knt_min
    min3=min_value[np.lexsort(min_value.T)][:17]#前3个最匹配的
    min3=min3.astype(int)
    # plt.plot(cur_data[:200],'b*-')
    # plt.plot(np.hstack(his[min3[0][0],min3[0][1]-30:min3[0][1]])[:200])
    # plt.plot(np.hstack(his[min3[1][0],min3[1][1]-30:min3[1][1]])[:200])
    # plt.plot(np.hstack(his[min3[2][0],min3[2][1]-30:min3[2][1]])[:200])
    # plt.show()
    # 取前三个的最小值作为预测值
    # prediction[day]=his[min3[0][0],min3[0][1]:min3[0][1]+30]
    # # print(min3)
    # for i in range(1,min3.shape[0]):
    #     prediction[day]=np.minimum(prediction[day],his[min3[i][0],min3[i][1]:min3[i][1]+30])
    # 求中位数
    temp=np.empty([17,30,132])
    for i in range(min3.shape[0]):
        temp[i]=his[min3[i][0],min3[i][1]:min3[i][1]+30]
    prediction[day]=np.mean(np.sort(temp,axis=0)[6:9],axis=0)


# 将结果保存为 .txt 文件
# prediction是预测值，6月份，8:00-9:00的数据，一共是30天，30个时间片，132条Link，30*30*132
filename = 'yun_20170729_evaluate.txt'
knt = 0
with open(filename, 'w') as f:
    for link in range(132):
        for day in range(30):
            for minute in range(0,60,2):

                if knt == 0:
                    knt += 1
                    temp = ''
                else:
                    temp = '\n'

                temp += Links2[link] + '#'
                date = '2016-05-'+str(day+1).zfill(2)
                temp += date + '#[' + date + ' 08:' + str(minute).zfill(2) + ':00,'
                if minute == 58:
                    temp += date+ ' 09:00:00)#'
                else:
                    temp += date+ ' 08:'+ str(minute + 2).zfill(2) + ':00)#'

                temp+= str(prediction[day,int(minute/2),link])

                f.write(temp)


yun_estimate_result.estimate_result('yun_true_data_MAY.txt',
                'yun_20170729_evaluate.txt',
                '0501','08:00-09:00',30)





























