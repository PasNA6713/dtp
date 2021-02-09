from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

from .models import *


# main page
def index(request):
    return render(request, 'main/analizator.html')

# about us page
def about(request):
    return render(request, 'main/about_us.html')

# log in
@csrf_exempt
def login(request):
    params = json.loads(request.body.decode("utf-8"))

    user = UserModel.objects.filter(login = params['login'], password = params['password'])
    admin = AdminModel.objects.filter(login = params['login'], password = params['password'])

    if admin:
        return JsonResponse('admin', safe=False)
    elif user:
        return JsonResponse('user', safe=False)
    else:
        return JsonResponse('not find', safe=False)


@csrf_exempt
def create_user(request):
    params = json.loads(request.body.decode("utf-8"))
    if params['permissons'] == 'Администратор':
        User = AdminModel(login = params['username'], password = params['password'])
    else:
        User = UserModel(login = params['username'], password = params['password'])
    User.save()
    return HttpResponse(status=200)
