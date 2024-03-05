from django import template

register = template.Library()


@register.filter(name='rate_converter')
def rate_converter(value):
    return int(round(number=value))
