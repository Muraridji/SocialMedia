from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'Користувач'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Адміністратор'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)

    def is_user(self):
        return self.role == self.USER

    def is_moderator(self):
        return self.role == self.MODERATOR

    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return self.username


class FriendshipRequest(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    send_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')


class Friendship(models.Model):
    user1 = models.ForeignKey(CustomUser, related_name='user1_friendship', on_delete=models.CASCADE)
    user2 = models.ForeignKey(CustomUser, related_name='user2_friendship', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    @staticmethod
    def are_friends(user1, user2):
        return (
                Friendship.objects.filter(user1=user1, user2=user2).exists() or
                Friendship.objects.filter(user1=user2, user2=user1).exists()
        )