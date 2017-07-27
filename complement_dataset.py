# -*- coding: utf-8 -*-
# @Time    : 2017/7/26 15:21
# @Author  : LiYun
# @File    : complement_dataset.py
'''description:
原始数据集有缺失，将缺失数据补上
'''

class complement_dataset(object):

    def __init__(self,infile,outfile,linkinfo):
        '''给定输入输出文件和link信息文件，将输入文件缺失的数据补齐并保存至输出文件，输出文件没有表头'''
        #每个月有几天,没有考虑闰年
        self.mdays=[31,28,31,30,31,30,31,31,30,31,30,31]
        #输入数据中每行元素的起始位置，分别为
        #link的结束位置，月，日，（起始时，分，秒），（终止时，分，秒），通行时间
        self.index=[19,25,28,43,46,49,63,66,69,73]
        #用一个列表来保存缺失值的索引
        self.lack=[]
        self.lackp=0
        #读取数据
        data=self.readdata(infile)
        #得到所有路段
        Links=self.get_all_links(linkinfo)
        #补充缺失数据
        data = self.generate(data,Links)
        #使用两边求最小法重新估计数据
        data=self.reestimate(data)
        #写数据
        self.writedata(outfile,data)

    def readdata(self, infile):
        '''从输入文件中读取数据，将数据存储在列表里并返回'''
        data = []
        with open(infile) as f:
            print(f.readline())
            while True:
                line = f.readline()
                if not line:
                    break
                data.append(line[:-1])
        return data

    def get_all_links(self,linkinfo):
        '''给定link信息文件，返回所有路段的名称'''
        Links=[]
        with open(linkinfo) as f:
            f.readline()
            while True:
                line=f.readline()
                if not line:
                    break
                Links.append(line[:self.index[0]])
        return sorted(Links)

    def generate(self,data,Links):
        data=sorted(data)
        #生成列表，原有的不变，添加没有的进去，返回排好序的数据
        pos=0
        for link in Links:
            for month in range(3,6): #3到5月份
                for day in range(1,self.mdays[month-1]+1):
                    for hour in range(24):
                        for minute in range(0,60,2):
                            pos=self.cmp_insert(link,month,day,hour,minute,data,pos)
            month=6 #6月份
            for day in range(1,self.mdays[month-1]+1):
                for hour in range(6,8):
                    for minute in range(0,60,2):
                        pos=self.cmp_insert(link,month,day,hour,minute,data,pos)
        return sorted(data)

    def cmp_insert(self,link,month,day,hour,minute,data,pos):
        date='2016-'+str(month).zfill(2)+'-'+str(day).zfill(2)
        date2=date
        begintime=str(hour).zfill(2)+':'+str(minute).zfill(2)+':00'
        if minute==58:
            if hour==23:
                if day==self.mdays[month-1]:
                    if month==12:
                        date2='2017-01-01'
                    else:
                        date2='2016-'+str(month+1).zfill(2)+'-01'
                else:
                    date2='2016-'+str(month).zfill(2)+'-'+str(day+1).zfill(2)
                endtime = '00:00:00'
            else:
                endtime=str(hour+1).zfill(2)+':00:00'
        else:
            endtime=str(hour).zfill(2)+':'+str(minute+2).zfill(2)+':00'
        x=link+';'+date+';['+date+' '+begintime+','+date2+' '+endtime+');'
        if x==data[pos][:self.index[9]]: #不缺失信息
            pos+=1
        else:
            data.append(x+'5.0')
            self.lack.append(self.lackp)
        self.lackp+=1
        return pos

    def reestimate(self,data):
        self.lackp=0
        for i,d in enumerate(data):
            if self.lackp<len(self.lack) and i==self.lack[self.lackp]:
                if self.lackp!=0 and self.lackp!=len(self.lack)-1:
                    if self.lack[self.lackp]!=self.lack[self.lackp-1]+1 and self.lack[self.lackp]!=self.lack[self.lackp+1]-1:
                        d=d[:73]+str(min(float(data[i-1][73:-1]),float(data[i+1][73:])))
                self.lackp+=1
            data[i]=d+'\n'
        return data

    def writedata(self,outfile,data):
        print(len(data))
        with open(outfile,'w',newline='') as f:
            f.writelines(data)


complement_dataset('gy_contest_link_traveltime_training_data.txt',
                     'yun_complement_dataset.txt',
                     'gy_contest_link_info.txt')
































