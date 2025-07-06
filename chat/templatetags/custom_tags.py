from django import template

register = template.Library()


@register.filter
def endswith(value, arg):
    if not value:
        return False
    return str(value).lower().endswith(arg.lower())