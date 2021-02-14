from math import sin, cos, sqrt, atan2, radians

import pandas as pd
import numpy as np

from sklearn.cluster import DBSCAN


def preprocc(jsn):
    df = pd.DataFrame(jsn)
    data = jsn
    
    df = df.rename(columns={'lat':'latitude','long':'longitude','region':'District','address':'street'})
    adress2 = []
    for i in data:
        try:
            adress2.append(i['address'].split(',')[1][1:])
        except:
            adress2.append(np.nan)
    df['street'] = adress2
    df = df.dropna()
    return df
    
def street_drob(a, mas):
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
    
def patrol_label(label, primer):
    def distance(lat1, lon1, lat2, lon2):
        R = 6373.0
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return (distance)

    dist_all = []
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
    dist_all = np.array(dist_all)
    primer['id'] = primer['id'].astype(str)
    primer.at[dist_all.argmin(), 'id'] = str([x for x in primer['id']]).replace('[','').replace(']','')
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
    
def raspredelenie_claster(street,patrol_number,df):
    def listsum(numList):
        
       if len(numList) == 1:
            return numList[0]
       else:
            return numList[0] + listsum(numList[1:])
    objct = df[df['street']==street]
    coords = objct[['latitude','longitude']].to_numpy()
    coord_patrol = pd.DataFrame(columns=['latitude','longitude'])
    schet = 0
    
    db = DBSCAN(eps=0.001,min_samples=1,algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    labels = np.unique(db.labels_)
    counts = np.unique(db.labels_,return_counts=True)[1]
    if patrol_number != 0:
        if len(labels) > patrol_number:
            total_counts = patrol_number
        else:
            total_counts = len(labels)

        total_labels = pd.DataFrame(counts)
        total_labels = total_labels.sort_values(by=0).index[-int(total_counts):]
        not_total_labels = [x for x in labels if x not in total_labels]


        df_coords = pd.DataFrame()
        df_coords['latitude'] = coords[:,0]
        df_coords['longitude'] = coords[:,1]
        df_coords['labels'] = db.labels_
        df_coords['id'] = [x for x in objct['id']]
        df_coords = df_coords.query('labels not in '+str(not_total_labels))

        for i in total_labels:
            a = patrol_label(i,df_coords)
            if a[0] != 0:
                coord_patrol.at[schet,'latitude'] = a[0]
                coord_patrol.at[schet,'longitude'] = a[1]
                coord_patrol.at[schet,'id'] = str(a[3])
                schet += 1
    return(coord_patrol)
    
def dynamic_patrol_func(patrol_number, df):
    coord_patrol = pd.DataFrame()
    dtp_count = 0
    
    # Кол-во патрулей по районам 
    dtp_count = len(df)
    if dtp_count == 0:
        return(0)
    patrol_count = pd.DataFrame()
    patrol_count['District'] = df['District'].unique()
    patrol_count['count_raion'] = ''
    for i in range(len(df.District.value_counts())):
        for j in range(len(patrol_count.District)):
            if (patrol_count.iloc[j]['District']) == (df.District.value_counts().index[i]):
                patrol_count.at[j,'count_raion'] = round((df.District.value_counts()[i]/dtp_count),2)
    for j in range(len(patrol_count.District)):
        if patrol_count.at[j,'count_raion']=='':
            patrol_count.at[j,'count_raion'] = 0
    patrol_count['count_raion'] = patrol_count['count_raion']*patrol_number
    buf_mas = street_drob(patrol_number,list(patrol_count['count_raion']))
    patrol_count['count_raion'] = buf_mas
    
    #распределение по улицам
    schet = 0
    for district in df.District.unique():
        if (patrol_count[patrol_count['District']==district].count_raion[schet] != 0):
            obj_dstr = df[df['District']==district]
            obj_dstr = obj_dstr.dropna(axis='index', how='any', subset=['street'])
            patrol_count_street = raspredelenie_street(obj_dstr,
                                                       round(patrol_count[patrol_count['District']==district].count_raion.values[0]))
            for i in range(len(patrol_count_street)):
                coord_buf = raspredelenie_claster(patrol_count_street.iloc[i][0],
                                                  patrol_count_street.iloc[i][1],df)
                coord_patrol = coord_patrol.append(coord_buf, ignore_index=True)  
        schet += 1
    coord_json = []
    for i in range(len(coord_patrol)):
        coord_json.append({'lat':coord_patrol.iloc[i,0],
                           'long':coord_patrol.iloc[i,1],
                           'points':[int(x.replace("'",'')) for x in coord_patrol.iloc[i,2].split(',')] })
                                    
    return coord_json


    