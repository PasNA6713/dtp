import datetime
import requests

from django.shortcuts import render
from  django.http import JsonResponse, HttpResponse
from wsgiref.util import FileWrapper
from django.views.decorators.csrf import csrf_exempt

from sklearn.cluster import DBSCAN
from django_pandas.managers import DataFrameManager
import pandas as pd

import json
import numpy as np
import random

from statist.models import *

from math import sin, cos, sqrt, atan2, radians

# ask DB with filter_params
def filter_dtp(dtps, params: dict) -> list:
    # filter by time
    if params['time'] != 5: 
        dtps = dtps.filter(time_group = params['time']-1)

    #  filter by weather
    if params['weather'] != 'Любая':
        dtps = dtps.filter(s_pog = params['weather'])

    # filter by month
    cur_month = params['month']
    if cur_month != 'Все время':
        if cur_month == 'Сентябрь': cur_month = 9
        elif cur_month == 'Октябрь': cur_month = 10
        elif cur_month == 'Ноябрь': cur_month = 11
        elif cur_month == 'Декабрь': cur_month = 12
        elif cur_month == 'Январь': cur_month = 1
        elif cur_month == 'Февраль': cur_month = 2
        elif cur_month == 'Март': cur_month = 3
        elif cur_month == 'Апрель': cur_month = 4
        elif cur_month == 'Май': cur_month = 5
        elif cur_month == 'Июнь': cur_month = 6
        elif cur_month == 'Июль': cur_month = 7
        elif cur_month == 'Август': cur_month = 8
        dtps = dtps.filter(date = cur_month)

    # filter by light
    light = params['light']
    if light != 'Не указано':
        if light == 'Освещение включено': 
            light = 'В темное время суток, освещение включено'
        if light == 'Освещение не включено': 
            light = 'В темное время суток, освещение не включено'
        if light == 'Освещение отсутствует': 
            light = 'В темное время суток, освещение отсутсвует'
        if light == 'Сумерки': 
            light = 'Сумерки'
        if light == 'День': 
            light = 'Светлое время суток'
        dtps = dtps.filter(osv = light)
        
    # filter by type
    if params['type'] != 'Не указан':
        dtps = dtps.filter(DTP_V = params['type'])

    # filter affected
    if params['affected'] != 'Не указано':
        if params['affected'] == 'Есть погибшие':
            dtps = dtps.exclude(POG = 0)
        if params['affected'] == 'Есть пострадавшие':
            dtps = dtps.filter(POG = 0)

    return dtps

@csrf_exempt
def load_data(request):
    params = json.loads(request.body.decode("utf-8"))
    data = pd.DataFrame(params['info'])
    file_location = 'result.xlsx'
    data.to_excel(file_location)

    try:    
        with open(file_location,  "r", encoding="utf8", errors='ignore') as f:
           file_data = f.read()
        response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="result.xlsx"'
    except IOError:
        response = HttpResponseNotFound('<h1>File not exist</h1>')
    return response

@csrf_exempt
def get_bd(region,city):
        def get_districts(city:str)->list:
            df = pd.read_csv('./data/regions.csv')
            regions = list(df[df['parent_name']==city]['code'])
            return regions

        def dates_generator():
            now = datetime.datetime.now()
            ctr = datetime.datetime(2018, 1, 1)
            dates_set = set()
            while ctr <= now:
                ctr += datetime.timedelta(days=1)
                dates_set.add(datetime.datetime(ctr.year, ctr.month, 1).strftime('%m.%Y'))
            return list(dates_set)
    
        dtp = pd.DataFrame(columns=[['date','Time','District','DTP_V','POG','RAN','K_TS','K_UCH','n_p','street','house',
                             'dor','factor','s_pog','s_pch','osv','COORD_W','COORD_L','OBJ_DTP','change_org_motion'
                             ]])
    
        dates = dates_generator()
        str_date = ''
        for i in dates:
            if i!=dates[len(dates)-1]:
                str_date += "MONTHS:"+i+","
            else:
                str_date += "MONTHS:"+i
                
        reg = get_districts(city)
        pay = dict()
        schet = 0
        for i in reg:
            print(str(i))
            pay["data"] = '{"date":["' + str_date + '"],\"ParReg\":\"' + str(region) + '\",\"order\":{\"type\":\"1\",\"fieldName\":\"dat\"},\"reg\":\"' + str(i) + '\",\"ind\":\"1\",\"st\":\"1\",\"en\":\"400\"}'
            r = requests.post("http://stat.gibdd.ru/map/getDTPCardData",json=pay)
            if r.status_code == 200:
                cards = json.loads(json.loads(r.content)["data"])["tab"]
            for i in range(len(cards)):
                dtp.loc[schet]=[
                    cards[i]['date'],cards[i]['Time'],cards[i]['District'],cards[i]['DTP_V'],
                    cards[i]['POG'], cards[i]['RAN'], cards[i]['K_TS'],    cards[i]['K_UCH'],
                    cards[i]['infoDtp']['n_p'],    cards[i]['infoDtp']['street'], cards[i]['infoDtp']['house'],
                    cards[i]['infoDtp']['dor'],    cards[i]['infoDtp']['factor'][0], cards[i]['infoDtp']['s_pog'][0],
                    cards[i]['infoDtp']['s_pch'],  cards[i]['infoDtp']['osv'],    cards[i]['infoDtp']['COORD_W'],
                    cards[i]['infoDtp']['COORD_L'],cards[i]['infoDtp']['OBJ_DTP'][0],cards[i]['infoDtp']['change_org_motion']
                   ]
                schet+=1
        return JsonResponse(dtp)

@csrf_exempt
def add_point(request):
    params = json.loads(request.body.decode("utf-8"))
    dtp = Dtp(latitude = params['latitude'], longitude = params['longitude'],
                RAN = params['RAN'], osv = params['osv'],
                DTP_V = params['DTP_V'], s_pog = params['s_pog'])
    dtp.save()
    return HttpResponse(status=200)

# change camera map
@csrf_exempt
def change_camera_map(request):
    params = json.loads(request.body.decode("utf-8"))

    if params['filter_params']['region'] == 'Санкт-Петербург':
        df1 = filter_dtp(PiterDtp.objects.all(), params['filter_params'])
    else:
        df1 = filter_dtp(Dtp.objects.all(), params['filter_params'])
    df2 = filter_dtp(Dtp_outside.objects.all(), params['filter_params'])

    if not params['camera_number']:
        cameras = get_cameras(df1, df2)
    elif params['location'] == 'Город':
        cameras = get_cameras_dinamic_inside(int(params['camera_number']), df1)
    else: 
        cameras = dinamic_cameras_func_outside(int(params['camera_number']), df2)

    response = {
        "cameras": cameras
    }
    return JsonResponse(response, safe=False)

# change heat map
@csrf_exempt
def change_heatmap(request):
    params = json.loads(request.body.decode("utf-8"))

    if params['filter_params']['region'] == 'Санкт-Петербург':
        df1 = filter_dtp(PiterDtp.objects.all(), params['filter_params'])
        df2 = []
    else:
        df1 = filter_dtp(Dtp.objects.all(), params['filter_params'])
        df2 = filter_dtp(Dtp_outside.objects.all(), params['filter_params'])

    dtps = [dict(i) for i in df1]
    dtps.extend([dict(i) for i in df2])

    response = {
        "placemarks": dtps
    }

    return JsonResponse(response, safe=False)


# init page
def present(request):
    return render(request, f'map/map.html')


# Clasterization
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
    primer.at[dist_all.argmin(), 'RAN'] = primer['RAN'].sum()
    primer.at[dist_all.argmin(), 'DTP_V'] = list(primer['DTP_V'])
    primer.at[dist_all.argmin(), 'POG'] = primer['POG'].sum()
    primer.at[dist_all.argmin(), 'factor'] = list(primer['factor'])
    primer.at[dist_all.argmin(), 'Time'] = list(primer['Time'])
    primer.at[dist_all.argmin(), 'osv'] = list(primer['osv'])
    primer.at[dist_all.argmin(), 's_pog'] = list(primer['s_pog'])
    if (dist_all.size == 0):
        return primer[primer['labels'] == label].iloc[0]
    else:
        return primer[primer['labels'] == label].iloc[dist_all.argmin()]

def get_cameras(df, df2):
    pogr = 0.2

    df = df.to_dataframe()
    df2 = df2.to_dataframe()

    def listsum(numList):

        if len(numList) == 1:
            return numList[0]
        else:
            return numList[0] + listsum(numList[1:])

    coord_patrol = pd.DataFrame(
        columns=[['latitude', 'longitude', 'labels', 'DTP_V', 'factor', 'POG', 'RAN', 'Time', 'osv', 's_pog']])
    index_street = 0
    schet = 0
    dtp_count = 0

    for street in df['street'].unique():
        objct = df[df['street'] == street]
        if objct.empty:
            continue
        coords = objct.as_matrix(columns=['latitude', 'longitude'])

        db = DBSCAN(eps=0.001, min_samples=3, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
        labels = np.unique(db.labels_)

        df_coords = pd.DataFrame()
        df_coords['latitude'] = coords[:, 0]
        df_coords['longitude'] = coords[:, 1]
        df_coords['labels'] = db.labels_
        df_coords['DTP_V'] = [x for x in objct['DTP_V']]
        df_coords['factor'] = [x for x in objct['factor']]
        df_coords['POG'] = listsum([x for x in objct['POG']])
        df_coords['RAN'] = listsum([x for x in objct['RAN']])
        df_coords['Time'] = [x for x in objct['Time']]
        df_coords['osv'] = [x for x in objct['osv']]
        df_coords['s_pog'] = [x for x in objct['s_pog']]

        for i in np.unique(db.labels_):
            a = patrol_label(i, df_coords, pogr)
            if a[0] != 0:
                coord_patrol.at[schet, 'latitude'] = a[0]
                coord_patrol.at[schet, 'longitude'] = a[1]
                coord_patrol.at[schet, 'DTP_V'] = str(a[3])
                coord_patrol.at[schet, 'factor'] = str(a[4])
                coord_patrol.at[schet, 'POG'] = a[5]
                coord_patrol.at[schet, 'RAN'] = a[6]
                coord_patrol.at[schet, 'Time'] = str(a[7])
                coord_patrol.at[schet, 'labels'] = index_street
                coord_patrol.at[schet, 'osv'] = str(a[8])
                coord_patrol.at[schet, 's_pog'] = str(a[9])
                schet += 1
        index_street += 1

    for street in df2['dor'].unique():
        objct = df2[df2['dor'] == street]
        if objct.empty:
            continue
        coords = objct.as_matrix(columns=['latitude', 'longitude'])

        db = DBSCAN(eps=0.001, min_samples=3, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
        labels = np.unique(db.labels_)

        df_coords = pd.DataFrame()
        df_coords['latitude'] = coords[:, 0]
        df_coords['longitude'] = coords[:, 1]
        df_coords['labels'] = db.labels_
        df_coords['DTP_V'] = [x for x in objct['DTP_V']]
        df_coords['factor'] = [x for x in objct['factor']]
        df_coords['POG'] = listsum([x for x in objct['POG']])
        df_coords['RAN'] = listsum([x for x in objct['RAN']])
        df_coords['Time'] = [x for x in objct['Time']]
        df_coords['osv'] = [x for x in objct['osv']]
        df_coords['s_pog'] = [x for x in objct['s_pog']]

        for i in np.unique(db.labels_):
            a = patrol_label(i, df_coords, pogr)
            if a[0] != 0:
                coord_patrol.at[schet, 'latitude'] = a[0]
                coord_patrol.at[schet, 'longitude'] = a[1]
                coord_patrol.at[schet, 'DTP_V'] = str(a[3])
                coord_patrol.at[schet, 'factor'] = str(a[4])
                coord_patrol.at[schet, 'POG'] = a[5]
                coord_patrol.at[schet, 'RAN'] = a[6]
                coord_patrol.at[schet, 'Time'] = str(a[7])
                coord_patrol.at[schet, 'labels'] = index_street
                coord_patrol.at[schet, 'osv'] = str(a[8])
                coord_patrol.at[schet, 's_pog'] = str(a[9])
                schet += 1
        index_street += 1

    spisok = []
    for i in range(len(coord_patrol)):
        spisok.append({
            "type":"Feature",
            "id": coord_patrol.iloc[i]['labels'][0],
            "geometry":{
                "type":"Point",
                "coordinates":[ coord_patrol.iloc[i]['latitude'][0], coord_patrol.iloc[i]['longitude'][0] ]
            },
            "properties": {
                    "clusterCaption": 'ДТП №' + str(coord_patrol.iloc[i]['labels'][0]+1).split('.')[0],
                    "balloonContent": coord_patrol.iloc[i]['DTP_V'][0].replace('[','').replace(']',' ').replace("'",'').strip(),
                    "hintContent": 'ДТП №' + str(coord_patrol.iloc[i]['labels'][0]+1).split('.')[0],

                    "factor": coord_patrol.iloc[i]['factor'][0].replace('[','').replace(']',' ').replace("'",'').strip(),
                    "POG": coord_patrol.iloc[i]['POG'][0],
                    "RAN": coord_patrol.iloc[i]['RAN'][0],
                    "Time": coord_patrol.iloc[i]['Time'][0].replace('[','').replace(']',' ').replace("'",'').strip(),
                    "osv": coord_patrol.iloc[i]['osv'][0].replace('[','').replace(']',' ').replace("'",'').strip(),
                    "s_pog": coord_patrol.iloc[i]['s_pog'][0].replace('[','').replace(']',' ').replace("'",'').strip()
            }
        })
    return (spisok)

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

def raspredelenie_claster(street, patrol_number, pogr, df):
    def listsum(numList):
        
       if len(numList) == 1:
            return numList[0]
       else:
            return numList[0] + listsum(numList[1:])
    objct = df[df['street']==street]
    coords = objct.as_matrix(columns=['latitude', 'longitude'])
    coord_patrol = pd.DataFrame(columns=[['latitude','longitude','labels','DTP_V','factor','POG','RAN','Time','osv','s_pog']])
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
        df_coords['DTP_V'] = [x for x in objct['DTP_V']]
        df_coords['factor'] = [x for x in objct['factor']]
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
                coord_patrol.at[schet,'factor'] = str(a[4])
                coord_patrol.at[schet,'POG'] = a[5]
                coord_patrol.at[schet,'RAN'] = a[6]
                coord_patrol.at[schet,'Time'] = str(a[7])
                coord_patrol.at[schet,'labels'] = index_street
                coord_patrol.at[schet,'osv'] = str(a[8])
                coord_patrol.at[schet,'s_pog'] = str(a[9])
                schet += 1
            index_street += 1
    return(coord_patrol)

def get_cameras_dinamic_inside(patrol_number, df):
    df = df.to_dataframe()
    pogr = 0.2
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
                                                  patrol_count_street.iloc[i][1],
                                                  pogr, df)
                coord_patrol = coord_patrol.append(coord_buf, ignore_index=True)  
        schet += 1

    counter = 0
    spisok = []
    for i in range(len(coord_patrol)):
        spisok.append({
            "type":"Feature",
            "id":counter,
            "geometry":{
                "type":"Point",
                "coordinates":[ coord_patrol.iloc[i]['latitude'][0], coord_patrol.iloc[i]['longitude'][0] ]
            },
            "properties": {
                    "clusterCaption": counter,
                    "balloonContent": coord_patrol.iloc[i]['DTP_V'][0],
                    "hintContent": counter,

                    "factor": coord_patrol.iloc[i]['factor'][0],
                    "POG": coord_patrol.iloc[i]['POG'][0],
                    "RAN": coord_patrol.iloc[i]['RAN'][0],
                    "Time": coord_patrol.iloc[i]['Time'][0],
                    "labels": coord_patrol.iloc[i]['labels'][0],
                    "osv": coord_patrol.iloc[i]['osv'][0],
                    "s_pog": coord_patrol.iloc[i]['s_pog'][0]
            }
        })
        counter += 1
    return (spisok)

def raspredelenie_street_outside(obj,patrol_number,df):
    
    dtp_count = 0
    print(obj)
    for i in obj['dor'].value_counts():
        dtp_count += i
    print(dtp_count)
    patrol_count_street = pd.DataFrame()
    patrol_count_street['dor'] = obj.dor.unique()
    patrol_count_street['count_patr'] = ''
    patrol_count_street = patrol_count_street.dropna()
    for i in range(len(obj.dor.value_counts())):
        for j in range(len(patrol_count_street['dor'])):
            if (patrol_count_street.iloc[j]['dor']) == (obj.dor.value_counts().index[i]):
                patrol_count_street.at[j,'count_patr'] = round(obj.dor.value_counts()[i]/dtp_count,1)*patrol_number
    print(patrol_count_street)
    buf_mas = street_drob(patrol_number,list(patrol_count_street['count_patr']))
    patrol_count_street['count_patr'] = buf_mas
    return(patrol_count_street)

def raspredelenie_claster_outside(street,patrol_number,pogr,df):
    
    def listsum(numList):
        
       if len(numList) == 1:
            return numList[0]
       else:
            return numList[0] + listsum(numList[1:])
    objct = df[df['dor']==street]
    coords = objct.as_matrix(columns=['latitude', 'longitude'])
    coord_patrol = pd.DataFrame(columns=[['latitude','longitude']])
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
        df_coords['factor'] = [x for x in objct['factor']]
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
                coord_patrol.at[schet,'factor'] = str(a[4])
                coord_patrol.at[schet,'POG'] = a[5]
                coord_patrol.at[schet,'RAN'] = a[6]
                coord_patrol.at[schet,'Time'] = str(a[7])
                coord_patrol.at[schet,'labels'] = index_street
                coord_patrol.at[schet,'osv'] = str(a[8])
                coord_patrol.at[schet,'s_pog'] = str(a[9])
                schet += 1
            index_street +=1
        print(coord_patrol)
    return(coord_patrol)

LAST_NUMBER = 0
LAST_RESPONSE = []
def dinamic_cameras_func_outside(patrol_number, df):
    global LAST_NUMBER
    global LAST_RESPONSE
    if patrol_number != LAST_NUMBER:
        df = [dict(i) for i in df]
        LAST_NUMBER = patrol_number
        LAST_RESPONSE = random.sample(df, patrol_number)
    return(LAST_RESPONSE)


def get_bd(region,city):
    
        def get_districts(city:str)->list:
            df = pd.read_csv('./data/regions.csv')
            regions = list(df[df['parent_name']==city]['code'])
            return regions

        def dates_generator():
            now = datetime.datetime.now()
            ctr = datetime.datetime(2018, 1, 1)
            dates_set = set()
            while ctr <= now:
                ctr += datetime.timedelta(days=1)
                dates_set.add(datetime.datetime(ctr.year, ctr.month, 1).strftime('%m.%Y'))
            return list(dates_set)
    
        dtp = pd.DataFrame(columns=[['date','Time','District','DTP_V','POG','RAN','K_TS','K_UCH','n_p','street','house',
                             'dor','factor','s_pog','s_pch','osv','COORD_W','COORD_L','OBJ_DTP','change_org_motion'
                             ]])
    
        dates = dates_generator()
        str_date = ''
        for i in dates:
            if i!=dates[len(dates)-1]:
                str_date += "MONTHS:"+i+","
            else:
                str_date += "MONTHS:"+i
                
        reg = get_districts(city)
        pay = dict()
        schet = 0
        for i in reg:
            print(str(i))
            pay["data"] = '{"date":["' + str_date + '"],\"ParReg\":\"' + str(region) + '\",\"order\":{\"type\":\"1\",\"fieldName\":\"dat\"},\"reg\":\"' + str(i) + '\",\"ind\":\"1\",\"st\":\"1\",\"en\":\"400\"}'
            r = requests.post("http://stat.gibdd.ru/map/getDTPCardData",json=pay)
            if r.status_code == 200:
                cards = json.loads(json.loads(r.content)["data"])["tab"]
            for i in range(len(cards)):
                dtp.loc[schet]=[
                    cards[i]['date'],cards[i]['Time'],cards[i]['District'],cards[i]['DTP_V'],
                    cards[i]['POG'], cards[i]['RAN'], cards[i]['K_TS'],    cards[i]['K_UCH'],
                    cards[i]['infoDtp']['n_p'],    cards[i]['infoDtp']['street'], cards[i]['infoDtp']['house'],
                    cards[i]['infoDtp']['dor'],    cards[i]['infoDtp']['factor'][0], cards[i]['infoDtp']['s_pog'][0],
                    cards[i]['infoDtp']['s_pch'],  cards[i]['infoDtp']['osv'],    cards[i]['infoDtp']['COORD_W'],
                    cards[i]['infoDtp']['COORD_L'],cards[i]['infoDtp']['OBJ_DTP'][0],cards[i]['infoDtp']['change_org_motion']
                   ]
                schet+=1
        return(dtp)