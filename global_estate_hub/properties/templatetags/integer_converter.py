from django import template

register = template.Library()


@register.filter(name='convert_to_int')
def convert_to_int(value):
    """
    Converts float to integer.

    value: float

    return: str
    """
    return int(value)
