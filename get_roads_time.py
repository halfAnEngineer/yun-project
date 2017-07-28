
import read_data
import datetime
import copy
import numpy as np
import pickle as pk
import pprint
#train_data=read_data.read_train_data('/home/hhb/Desktop/road/data/Untitled Document.txt')
#这个函数是把所有训练数据读取出来，然后提取关键信息存到列表里面，
train_data=read_data.read_train_data('/home/hhb/Desktop/road/data/gy_contest_link_traveltime_training_data.txt')
# output = open('data.pkl', 'wb')
# pk.dump(train_data, output,2)
# output.close()
# pkl_file = open('data.pkl', 'rb')
# data = pk.load(pkl_file)
# pprint.pprint(data)
# print(data)
#下面这个函数是输出特定的路段特定时间段的情况
#train_data 训练数据的列表
#roads_id 需要取出的道路的id列表
#start_time 需要取出信息的道路的起始时间列表
#end_time 需要取出信息的道路的结束时间列表
#返回值 所有需要取出信息的路段的信息
def get_roads_message(train_data,roads_id,start_time,end_time):
    data=[]
    for road,st,et in zip(roads_id,start_time,end_time):
        road_data=[x for x in train_data if x['time_start']>=st and x['time_end']<=et and x['road_id']==road]
        data.append(copy.deepcopy(road_data))
    return data
#使用范例
#get_roads_message(train_data,['3377906280028510514'],[datetime.datetime(2016,6,1,8,0)],[datetime.datetime(2016,6,10,8,2)])
# def num_to_time(month,day,hour,minute,year=2016,second=0):
#     time_string=str('%04d'%year+'-'+'%02d'%month+'-'+'%02d'%day+' '+'%02d'%hour+':'+'%02d'%minute+':'+'%02d'%second)
#     time=datetime.datetime.strptime(time_string,'%Y-%m-%d %H:%M:%S')
#     return time