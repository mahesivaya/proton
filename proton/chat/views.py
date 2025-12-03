from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Room, Message, DirectMessage

User = get_user_model()


# ----------------------------------------------------
# MAIN CHAT PAGE
# ----------------------------------------------------
@login_required
def clinic_chat_page(request):
    return render(request, "chat/clinic_chat.html")


# ----------------------------------------------------
# ROOM HISTORY
# ----------------------------------------------------
@login_required
def chat_history(request, room_name):
    room, _ = Room.objects.get_or_create(name=room_name)
    qs = Message.objects.filter(room=room).select_related("user").order_by("timestamp")

    data = [
        {
            "username": m.user.username,
            "message": m.content,
            "timestamp": m.timestamp.isoformat(),
        }
        for m in qs
    ]
    return JsonResponse(data, safe=False)


# ----------------------------------------------------
# DM HISTORY
# ----------------------------------------------------
@login_required
def dm_history(request, username):
    other = get_object_or_404(User, username=username)

    qs = DirectMessage.objects.filter(
        Q(sender=request.user, receiver=other) |
        Q(sender=other, receiver=request.user)
    ).select_related("sender").order_by("timestamp")

    data = [
        {
            "username": m.sender.username,
            "message": m.content,
            "timestamp": m.timestamp.isoformat(),
        }
        for m in qs
    ]
    return JsonResponse(data, safe=False)


# ----------------------------------------------------
# USER LIST
# ----------------------------------------------------
@login_required
def user_list(request):
    users = list(User.objects.values_list("username", flat=True))
    return JsonResponse(users, safe=False)


# ----------------------------------------------------
# CREATE ROOM
# ----------------------------------------------------
@login_required
@csrf_exempt
def create_room(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    data = json.loads(request.body)
    name = data.get("name", "").strip().lower()

    if not name:
        return JsonResponse({"error": "Room name required"}, status=400)

    if Room.objects.filter(name=name).exists():
        return JsonResponse({"error": "Room already exists"}, status=400)

    room = Room.objects.create(name=name, created_by=request.user)
    room.users.add(request.user)

    return JsonResponse({"success": True, "room": name})


# ----------------------------------------------------
# ROOM LIST
# ----------------------------------------------------
# @login_required
# def room_list(request):
#     rooms = list(Room.objects.values_list("name", flat=True))

#     return JsonResponse(rooms, safe=False)

@login_required
def room_list(request):
    data = []

    for room in Room.objects.all():
        data.append({
            "name": room.name,
            "is_user": request.user in room.users.all(),
        })

    return JsonResponse(data, safe=False)


# ----------------------------------------------------
# ROOM USERS
# ----------------------------------------------------
@login_required
def room_users(request, room_name):
    try:
        room = Room.objects.get(name=room_name)
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)

    users = list(room.users.values_list("username", flat=True))
    creator = room.created_by.username if room.created_by else "Unknown"

    return JsonResponse({
        "created_by": creator,
        "users": users,
    })


# ----------------------------------------------------
# JOIN ROOM
# ----------------------------------------------------
@login_required
def join_room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    room.users.add(request.user)
    return JsonResponse({"joined": True})


# ----------------------------------------------------
# ROOM INFO (BUG FIXED)
# ----------------------------------------------------

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

active_rooms = {}

@login_required
def room_info(request, room_name):
    try:
        room = Room.objects.get(name=room_name)
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)

    # Historical users (saved in DB)
    all_users = list(room.users.values_list("username", flat=True))

    # Creator
    creator = room.created_by.username if room.created_by else None

    # Active users (WebSocket)
    active = list(active_rooms.get(room_name, []))

    return JsonResponse({
        "room": room.name,
        "created_by": creator,
        "users_all": all_users,      # all users who ever joined
        "users_active": active       # only currently active users
    })
