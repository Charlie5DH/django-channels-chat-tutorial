from django.shortcuts import render
from chat.models import Room, Message
from django.http import HttpResponse

# Create your views here.
# Since we are using channels, we are not using the Django's built-in views.
# Instead, we will use the consumers to handle the inputs and output of messages.
# our consumers will store the data in the database and will serve the data to the frontend.

def index_view(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.all(),
    })


def room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'room.html', {
        'room': chat_room,
    })

def get_all_messages(request):
    if request.method == 'GET':
        messages = Message.objects.all()
        return HttpResponse(messages)