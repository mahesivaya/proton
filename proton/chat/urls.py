# chat/urls.py
from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.clinic_chat_page, name="clinic_chat"),

    # room management
    path("rooms/", views.room_list, name="room_list"),
    path("rooms/create/", views.create_room, name="create_room"),

    # History
    # path("history/", views.chat_history, name="chat_history"),
    path("history/<str:room_name>/", views.chat_history, name="chat_history"),

    #DM
    path("dm/history/<str:username>/", views.dm_history, name="dm_history"),
    path("users/", views.user_list, name="user_list"),
]
