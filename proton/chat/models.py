# chat/models.py
from django.db import models
from django.conf import settings


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_rooms")
    users = models.ManyToManyField(CustomUser, related_name="rooms_joined", blank=True)
    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.user} @ {self.room}: {self.content[:20]}"


class DirectMessage(models.Model):
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="sent_dms"
    )
    receiver = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="received_dms"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}"

class ChatMessage(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"[{self.timestamp}] {self.username}: {self.message[:30]}"

