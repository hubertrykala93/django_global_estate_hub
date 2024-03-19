from django import template
from unidecode import unidecode

register = template.Library()


@register.filter(name='unicode_filter')
def unicode_filter(value) -> str:
    """
    Translates non-English letters into English letters.

    value: str

    return: str
    """
    return unidecode(value)
