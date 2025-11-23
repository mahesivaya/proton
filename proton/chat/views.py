from django.shortcuts import render

# Create your views here.
from accounts.decorators import role_required
from django.contrib.auth.decorators import login_required

@role_required(allowed_roles=['reception', 'admin', 'doctor'])
@login_required
def chat(request):
    return render(request, "chat/chat.html", {
        "room_name": "clinic_chat",
        "username": request.user.username,
    })


from django.http import JsonResponse
from .models import ChatMessage

def get_chat_history(request):
    messages = ChatMessage.objects.order_by('timestamp').values(
        'username__username', 'message', 'timestamp'
    )

    data = [
        {
            "username": msg["username__username"] or "Guest",
            "message": msg["message"],
            "timestamp": msg["timestamp"].strftime("%Y-%m-%d %H:%M"),
        }
        for msg in messages
    ]

    return JsonResponse(data, safe=False)
