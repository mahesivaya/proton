# chat/views.py
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model

from .models import Room, Message, DirectMessage

User = get_user_model()


@login_required
def clinic_chat_page(request):
    # template you showed, e.g. templates/chat/clinic_chat.html
    return render(request, "chat/clinic_chat.html")


@login_required
def chat_history(request, room_name):
    room, _ = Room.objects.get_or_create(name=room_name)
    qs = Message.objects.filter(room=room).select_related("user").order_by("timestamp")[:200]

    data = [
        {
            "username": m.user.username,
            "message": m.content,
            "timestamp": m.timestamp.isoformat(),
        }
        for m in qs
    ]
    return JsonResponse(data, safe=False)


@login_required
def dm_history(request, username):
    other = get_object_or_404(User, username=username)

    qs = DirectMessage.objects.filter(
        Q(sender=request.user, receiver=other) | Q(sender=other, receiver=request.user)
    ).select_related("sender").order_by("timestamp")[:200]

    data = [
        {
            "username": m.sender.username,
            "message": m.content,
            "timestamp": m.timestamp.isoformat(),
        }
        for m in qs
    ]
    return JsonResponse(data, safe=False)


@login_required
def user_list(request):
    users = User.objects.values_list("username", flat=True)
    return JsonResponse(list(users), safe=False)


from django.views.decorators.csrf import csrf_exempt
import json

@login_required
@csrf_exempt
def create_room(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        name = body.get("name", "").strip()

        if not name:
            return JsonResponse({"error": "Room name required"}, status=400)

        if Room.objects.filter(name=name).exists():
            return JsonResponse({"error": "Room already exists"}, status=409)

        room = Room.objects.create(name=name)
        return JsonResponse({"success": True, "room": room.name})

    return JsonResponse({"error": "POST only"}, status=405)


@login_required
def room_list(request):
    rooms = Room.objects.values_list("name", flat=True)
    return JsonResponse(list(rooms), safe=False)
