from django import template

register = template.Library()


@register.filter
def replace_filter(value):
    return value.replace('-', ' ')
