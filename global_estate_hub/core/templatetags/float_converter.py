import re

from django import template

register = template.Library()


@register.filter(name='float_converter')
def float_converter(value):
    """
    Converts float to integer

    value: float

    return: int
    """
    return int(value)


@register.filter(name='convert_to_str')
def convert_to_str(value):
    return str(value)


@register.filter(name='add_dots')
def add_dots(value):
    return value
