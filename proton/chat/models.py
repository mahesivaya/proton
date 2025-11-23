from django.db import models
# from django.contrib.auth.models import User

from accounts.models import CustomUser

class ChatMessage(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"[{self.timestamp}] {self.username}: {self.message[:30]}"
