from django import template

register = template.Library()


@register.filter(name='convert_to_int')
def convert_to_int(value) -> int:
    """
    Converts float to integer.

    value: float

    return: int
    """
    return int(value)
