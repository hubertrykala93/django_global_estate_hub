from .models import Property


def featured_properties(request) -> dict:
    """
    Returns three featured properties sorted by date.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        dict
    """
    return {
        "featured_properties": Property.objects.filter(is_featured=True).order_by(
            "-date_posted"
        )[:3]
    }
