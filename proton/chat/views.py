from django.shortcuts import render

# Create your views here.
from accounts.decorators import role_required
from django.contrib.auth.decorators import login_required

@role_required(allowed_roles=['reception', 'admin', 'doctor'])
@login_required
def chat_room(request):
    return render(request, "chat/chat.html", {
        "room_name": "clinic_chat",
        "username": request.user.username,
    })
