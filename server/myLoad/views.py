from django.shortcuts import render


def start(request):
    return render(request, 'pages/start.html',  {'show_buttons': True})

def settings(request):
    return render(request, 'pages/settings.html')



