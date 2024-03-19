from django import template

register = template.Library()


@register.simple_tag(name='url_replace')
def url_replace(request, page, number) -> str:
    """
    Template tag for pagination.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        page: django.utils.safestring.SafeString
        number: int

    Returns
    ----------
        dict
    """
    dict_ = request.GET.copy()
    dict_[page] = number

    return dict_.urlencode()
