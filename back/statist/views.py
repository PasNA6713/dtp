from django.shortcuts import render
from .models import Dtp


def graph(request):
    qs = Dtp.objects.all()
    data = qs.to_dataframe()
    katas = [(i) for i in data.Time.value_counts()]
    katas_lb = [(i) for i in data.Time.value_counts().index]
    tim = [(i) for i in data.Time.value_counts()[:10]]
    tim_lb = [i for i in data.Time.value_counts()[:10].index]
    sez = [i for i in data.date.value_counts()]
    sez_lb = [i for i in data.date.value_counts().index]
    for i in range(len(sez_lb)):
        if sez_lb[i]=='0':
           sez_lb[i]='Январь'
        if sez_lb[i]=='1':
            sez_lb[i]='Февраль'
        if sez_lb[i]=='2':
           sez_lb[i]='Март'
        if sez_lb[i]=='3':
            sez_lb[i]='Апрель'
        if sez_lb[i]=='4':
            sez_lb[i]='Май'
        if sez_lb[i]=='5':
            sez_lb[i]='Июнь'
        if sez_lb[i]=='6':
           sez_lb[i]='Июль'
        if sez_lb[i]=='7':
            sez_lb[i]='Авгутс'
        if sez_lb[i]=='8':
           sez_lb[i]='Сентябрь'
        if sez_lb[i]=='9':
            sez_lb[i]='Октябрь'
        if sez_lb[i]=='10':
            sez_lb[i]='Ноябрь'
        if sez_lb[i]=='11':
            sez_lb[i]='Декабрь'
    osv = [i for i in data.osv.value_counts()]
    osv_lb = [i for i in data.osv.value_counts().index]
    dtp = [i for i in data.DTP_V.value_counts()[:5]]
    dtp_lb = [i for i in data.DTP_V.value_counts()[:5].index]
    pog = [i for i in data.s_pog.value_counts()]
    pog_lb = [i for i in data.s_pog.value_counts().index]
    pch = [i for i in data.s_pch.value_counts()]
    pch_lb = [i for i in data.s_pch.value_counts().index]

    context = {
        'df': data,
        'katas': katas,
        'katas_lb': katas_lb,
        'tim': tim,
        'tim_lb': tim_lb,
        'sez': sez,
        'sez_lb': sez_lb,
        'osv': osv,
        'osv_lb': osv_lb,
        'dtp': dtp,
        'dtp_lb': dtp_lb,
        'pog': pog,
        'pog_lb': pog_lb,
        'pch': pch,
        'pch_lb': pch_lb

    }
    return render(request, 'statist/untitled-2.html', context)





