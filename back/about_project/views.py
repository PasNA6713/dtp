from django.shortcuts import render

def inform(request):
    return render(request, 'about_project/about_project.html')


def about(request):
    return render(request, 'main/about_us.html')