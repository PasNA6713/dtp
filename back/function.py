import pandas as pd
import numpy as np
from sklearn.neighbors import DistanceMetric
from sklearn.cluster import DBSCAN


#ЭТО РАССТОЯНИЕ МЕЖДУ ТОЧКАМИ
def distance(latitude1, longitude1, latitude12, longitude2):


    return (dist.pairwise(
        np.radians([[latitude1, longitude1]]),
        np.radians([[latitude12, longitude2]])
    ) * earth_radius)[0][0]
###########################################################


#ОКРУГЛЕНИЕ ЕБАННЫХ ДРОБЕЙ
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
################################################################



# ВЫЧИСЛЕНИЕ КООРДИНАТ ДЛЯ КЛАСТЕРОВ
def patrol_label(label, primer, pogr):


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
    if (dist_all.size == 0):
        return primer[['latitude', 'longitude']][primer['labels'] == label].iloc[0]
    else:
        return primer[['latitude', 'longitude']][primer['labels'] == label].iloc[dist_all.argmin()]
######################################################################################################



# РАСПРЕДЕЛЕНИЕ ПАТРУЛЕЙ ПО УЛИЦАМ
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
#####################################################################################################################



# РАСПРЕДЕЛЕНИЕ ПАТРУЛЕЙ ПО КЛАСТЕРАМ
def raspredelenie_claster(street, patrol_number, pogr):


    objct = df[df['street'] == street]
    coords = objct.as_matrix(columns=['latitude', 'longitude'])
    coord_patrol = pd.DataFrame(columns=[['latitude', 'longitude']])
    schet = 0

    db = DBSCAN(eps=0.001, min_samples=2, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    labels = np.unique(db.labels_)
    counts = np.unique(db.labels_, return_counts=True)[1]
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
        df_coords['latitude'] = coords[:, 0]
        df_coords['longitude'] = coords[:, 1]
        df_coords['labels'] = db.labels_
        df_coords = df_coords.query('labels not in ' + str(not_total_labels))

        for i in total_labels:
            a = patrol_label(i, df_coords, pogr)
            if a[0] != 0:
                coord_patrol.at[schet, 'latitude'] = a[0]
                coord_patrol.at[schet, 'longitude'] = a[1]
                schet += 1
        print(coord_patrol)
    return (coord_patrol)
############################################################################################################



# ВЫВОД КООРДИНАТ
def dinamic_patrol_func(df: list, pogr: float, patrol_number: int) -> list:


    dist = DistanceMetric.get_metric('haversine')
    earth_radius = 6371
    coord_patrol = pd.DataFrame()
    dtp_count = 0
    pogr = 0.2
    # Кол-во патрулей по районам
    dtp_count = len(df)
    if dtp_count == 0:
        return (0)
    patrol_count = pd.DataFrame()
    patrol_count['District'] = df['District'].unique()
    patrol_count['count_raion'] = ''
    for i in range(len(df.District.value_counts())):
        for j in range(len(patrol_count.District)):
            if (patrol_count.iloc[j]['District']) == (df.District.value_counts().index[i]):
                patrol_count.at[j, 'count_raion'] = round(
                    (df.District.value_counts()[i] / dtp_count), 2)
    patrol_count['count_raion'] = patrol_count['count_raion'] * patrol_number

    # распределение по улицам
    schet = 0
    for district in df.District.unique():
        if (patrol_count[patrol_count['District'] == district].count_raion[schet] != 0):
            obj_dstr = df[df['District'] == district]
            obj_dstr = obj_dstr.dropna(axis='index', how='any', subset=['street'])
            patrol_count_street = raspredelenie_street(obj_dstr,
                                                       round(patrol_count[patrol_count['District'] == district].count_raion.values[0]))
            for i in range(len(patrol_count_street)):
                print(patrol_count_street.iloc[i][0])
                print(round(patrol_count_street.iloc[i][1]))
                coord_buf = raspredelenie_claster(patrol_count_street.iloc[i][0],
                                                  patrol_count_street.iloc[i][1],
                                                  pogr)
                coord_patrol = coord_patrol.append(coord_buf, ignore_index=True)
        schet += 1
    return (coord_patrol)
#######################################################################################################