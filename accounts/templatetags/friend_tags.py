from django import template
from accounts.models import Friendship

register = template.Library()

@register.filter
def are_friends(user1, user2):
    return Friendship.are_friends(user1, user2)


@register.filter
def received_request(user1, user2):
    return user1.received_requests.filter(sender=user2).exists()