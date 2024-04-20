from django import template

register = template.Library()


@register.filter(name="price_converter")
def price_converter(value) -> str:
    """
    Converts float to integer, then adds a separator in the form of a dot in the property price.

    Parameters
    ----------
        value: float

    Returns
    ----------
        str
    """
    return format(int(value), ",d").replace(",", ".")
