from django.db import models
from django.conf import settings


class Chat(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)  # Для группового чата обязателен
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="chats")
    avatar = models.FileField(upload_to="chats/", blank=True, null=True)
    group_chat = models.BooleanField(default=False)
    community = models.BooleanField(default=False)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='admin_chats', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.community:
            self.group_chat = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name if self.group_chat else f"Private chat {self.id}"

    def is_admin(self, user):
        return self.admins.filter(id=user.id).exists()


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    media = models.FileField(upload_to="chat_media/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    from_community = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} → {self.chat}: {self.content[:30]}"

