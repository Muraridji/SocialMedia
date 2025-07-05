from django import template

register = template.Library()

@register.filter(name='custom_filter')
def custom_filter(value):
    return f"custom: {value}"