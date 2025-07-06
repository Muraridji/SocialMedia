from django import template

register = template.Library()

@register.filter(name='custom_filter')
def custom_filter(value):
    return f"custom: {value}"

@register.filter(name='add_class')
def add_class(value, css_class):
    return value.as_widget(attrs={"class": css_class})