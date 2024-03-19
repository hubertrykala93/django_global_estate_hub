from django import template

register = template.Library()


@register.filter(name='rate_converter')
def rate_converter(value) -> int:
    """
    Rounds and converts the value to an integer.

    values: float

    return: int
    """
    return int(round(number=value))
