from django.shortcuts import render


def start(request):
    return render(request, 'pages/start.html',  {'show_buttons': True})

def settings(request):
    return render(request, 'pages/settings.html')

def start_meeting(request):
    room_name = "myload"
    return render(request, 'pages/start_meeting.html', {'room_name': room_name})

