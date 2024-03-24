from django import template
from unidecode import unidecode

register = template.Library()


@register.filter(name='convert_to_int')
def convert_to_int(value) -> int:
    """
    Converts float to integer.

    Parameters
    ----------
        value: float

    Returns
    ----------
        int
    """
    return int(value)


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


@register.filter(name='unicode_filter')
def unicode_filter(value) -> str:
    """
    Translates non-English letters into English letters.

    Parameters
    ----------
        value: str

    Returns
    ----------
        return: str
    """
    return unidecode(value)
