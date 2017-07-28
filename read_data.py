import time
import copy
import datetime
#
# const_roads_name_path='/home/hhb/Desktop/road/data/gy_contest_link_info.txt'
# def get_roadname(file_path):
#     roads_name=[]
#     with open(file_path) as f:
#         line = f.readline()
#         while True:
#             line = f.readline()
#             if not line:
#                 break
#             roads_name.append(line.split(';')[0])
#         return roads_name
# name=get_roadname(const_roads_name_path)

def read_train_data(file_path):
    train_data=[]
    with open(file_path) as f:
        line = f.readline()
        while True:
            temp={}
            line = f.readline()
            if not line:
                break
            R_message = line.split(';')
            temp['road_id']=R_message[0]
            temp['date'] = datetime.datetime.strptime(R_message[1], '%Y-%m-%d')
            time = R_message[2][1:-1].split(',')
            temp['time_start'] = datetime.datetime.strptime(time[0], '%Y-%m-%d %H:%M:%S')
            temp['time_end'] = datetime.datetime.strptime(time[1], '%Y-%m-%d %H:%M:%S')
            temp['pass_time']=float(R_message[3])
            train_data.append(copy.deepcopy(temp))
    return train_data
