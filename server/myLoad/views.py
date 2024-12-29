from django.shortcuts import render


def start(request):
    return render(request, 'start.html')

def settings(request):
    return render(request, 'settings.html')



