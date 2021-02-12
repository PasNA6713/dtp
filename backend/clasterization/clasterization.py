import time
from math import sin, cos, sqrt, atan2, radians

import pandas as pd
import numpy as np

from sklearn.cluster import DBSCAN


def street_drob(a,mas):

    buf = a
    for i in range(len(mas)):
        if mas[i]>1:
            mas[i] = round(mas[i])
            buf = buf - mas[i]
    buf_mas = [x for x in mas if x < 1]
    for j in range(len(mas)):
        for i in range(len(mas)):
            if mas[i]<1 and mas[i] == max(buf_mas) and buf != 0:
                mas[i] = 1
                buf_mas = [x for x in mas if x < 1]
                buf = buf - 1
    for i in range(len(mas)):
        if mas[i]<1:
            mas[i]=0
    return(mas)

def patrol_label(label, primer, pogr):

    def distance(lat1, lon1, lat2, lon2):
        R = 6373.0
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return (distance)

    dist_all = []
    print(len(primer[['latitude', 'longitude']][primer['labels'] == label]))
    start_time = time.time()
    for i in range(len(primer[['latitude', 'longitude']][primer['labels'] == label])):
        sum_dist = 0
        for j in range(len(primer[['latitude', 'longitude']][primer['labels'] == label])):
            dist = distance(
                primer[['latitude', 'longitude']][primer['labels'] == label].iloc[i][0],
                primer[['latitude', 'longitude']][primer['labels'] == label].iloc[i][1],
                primer[['latitude', 'longitude']][primer['labels'] == label].iloc[j][0],
                primer[['latitude', 'longitude']][primer['labels'] == label].iloc[j][1]
            )
            sum_dist += dist
        dist_all.append(sum_dist)
    print('обработка')
    print(time.time()-start_time)
    dist_all = np.array(dist_all)
    primer.at[dist_all.argmin(), 'RAN'] = primer['RAN'].sum()
    primer.at[dist_all.argmin(), 'DTP_V'] = list(primer['DTP_V'])
    primer.at[dist_all.argmin(), 'POG'] = primer['POG'].sum()
    primer.at[dist_all.argmin(), 'Time'] = list(primer['Time'])
    primer.at[dist_all.argmin(), 'osv'] = list(primer['osv'])
    primer.at[dist_all.argmin(), 's_pog'] = list(primer['s_pog'])
    if (dist_all.size == 0):
        return primer[primer['labels'] == label].iloc[0]
    else:
        return primer[primer['labels'] == label].iloc[dist_all.argmin()]

def raspredelenie_street(obj,patrol_number):
    dtp_count = 0
    for i in obj.street.value_counts():
        dtp_count += i
    patrol_count_street = pd.DataFrame()
    patrol_count_street['street'] = obj.street.unique()
    patrol_count_street['count_patr'] = ''
    for i in range(len(obj.street.value_counts())):
        for j in range(len(patrol_count_street['street'])):
            if (patrol_count_street.iloc[j]['street']) == (obj.street.value_counts().index[i]):
                patrol_count_street.at[j,'count_patr'] = round(obj.street.value_counts()[i]/dtp_count,1)*patrol_number
    buf_mas = street_drob(patrol_number,list(patrol_count_street['count_patr']))
    patrol_count_street['count_patr'] = buf_mas
    return(patrol_count_street)

def raspredelenie_claster(street,patrol_number,pogr,month,itl_time,df):    
    def listsum(numList):
        
       if len(numList) == 1:
            return numList[0]
       else:
            return numList[0] + listsum(numList[1:])
    objct = df[df['street']==street][df['date']==month][df['Time_Group']==itl_time]
    coords = objct[['latitude','longitude']].to_numpy()
    coord_patrol = pd.DataFrame(columns=['latitude','longitude','labels','DTP_V','POG','RAN','Time','osv','s_pog'])
    schet = 0
    
    db = DBSCAN(eps=0.001,min_samples=1,algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    labels = np.unique(db.labels_)
    counts = np.unique(db.labels_,return_counts=True)[1]
    if patrol_number != 0:
        if len(labels) > patrol_number:
            total_counts = patrol_number
        else:
            total_counts = len(labels)

        print(total_counts)
        total_labels = pd.DataFrame(counts)
        total_labels = total_labels.sort_values(by=0).index[-int(total_counts):]
        not_total_labels = [x for x in labels if x not in total_labels]


        df_coords = pd.DataFrame()
        df_coords['latitude'] = coords[:,0]
        df_coords['longitude'] = coords[:,1]
        df_coords['labels'] = db.labels_
        df_coords['DTP_V'] = [x for x in objct['DTP_V']]
        df_coords['POG'] = listsum([x for x in objct['POG']])
        df_coords['RAN'] = listsum([x for x in objct['RAN']])
        df_coords['Time'] = [x for x in objct['Time']]
        df_coords['osv'] = [x for x in objct['osv']]
        df_coords['s_pog'] = [x for x in objct['s_pog']]
        df_coords = df_coords.query('labels not in '+str(not_total_labels))

        index_street = 0
        for i in total_labels:
            a = patrol_label(i,df_coords,pogr)
            if a[0] != 0:
                coord_patrol.at[schet,'latitude'] = a[0]
                coord_patrol.at[schet,'longitude'] = a[1]
                coord_patrol.at[schet,'DTP_V'] = str(a[3])
                coord_patrol.at[schet,'POG'] = a[4]
                coord_patrol.at[schet,'RAN'] = a[5]
                coord_patrol.at[schet,'Time'] = str(a[6])
                coord_patrol.at[schet,'labels'] = index_street
                coord_patrol.at[schet,'osv'] = str(a[7])
                coord_patrol.at[schet,'s_pog'] = str(a[8])
                schet += 1
            index_street += 1
        print(coord_patrol)
    return(coord_patrol)

def dinamic_patrol_func(itl_time,month,pogr,patrol_number,df):
   
 
    coord_patrol = pd.DataFrame()
    dtp_count = 0
    
    # Кол-во патрулей по районам 
    dtp_count = len(df[df['Time_Group']==itl_time][df['date']==month])
    if dtp_count == 0:
        return(0)
    patrol_count = pd.DataFrame()
    patrol_count['District'] = df['District'].unique()
    patrol_count['count_raion'] = ''
    for i in range(len(df.District[df['Time_Group']==itl_time][df['date']==month].value_counts())):
        for j in range(len(patrol_count.District)):
            if (patrol_count.iloc[j]['District']) == (df.District.value_counts().index[i]):
                patrol_count.at[j,'count_raion'] = round((df.District[df['Time_Group']==itl_time][df['date']==month].value_counts()[i]/dtp_count),2)
    for j in range(len(patrol_count.District)):
        if patrol_count.at[j,'count_raion']=='':
            patrol_count.at[j,'count_raion'] = 0
    patrol_count['count_raion'] = patrol_count['count_raion']*patrol_number
    buf_mas = street_drob(patrol_number,list(patrol_count['count_raion']))
    patrol_count['count_raion'] = buf_mas
    print(patrol_count)
    
    #распределение по улицам
    schet = 0
    for district in df.District.unique():
        print('_________________________________________'+district+'______________________________________')
        if (patrol_count[patrol_count['District']==district].count_raion[schet] != 0):
            obj_dstr = df[df['District']==district][df['date']==month][df['Time_Group']==itl_time]
            obj_dstr = obj_dstr.dropna(axis='index', how='any', subset=['street'])
            patrol_count_street = raspredelenie_street(obj_dstr,
                                                       round(patrol_count[patrol_count['District']==district].count_raion.values[0]))
            print(patrol_count_street)
            for i in range(len(patrol_count_street)):
                print(patrol_count_street.iloc[i][0])
                print(round(patrol_count_street.iloc[i][1]))
                coord_buf = raspredelenie_claster(patrol_count_street.iloc[i][0],
                                                  patrol_count_street.iloc[i][1],
                                                  pogr,month,itl_time,df)
                coord_patrol = coord_patrol.append(coord_buf, ignore_index=True)  
        schet += 1
    return(coord_patrol)
        

def claster():
    pass