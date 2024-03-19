from django import template

register = template.Library()


@register.filter(name='rate_converter')
def rate_converter(value) -> int:
    """
    Rounds and converts the value to an integer.

    Parameters
    ----------
        values: float

    Returns
    ----------
        int
    """
    return int(round(number=value))
