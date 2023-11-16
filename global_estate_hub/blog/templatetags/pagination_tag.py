from django import template

register = template.Library()


@register.simple_tag(name='url_replace')
def url_replace(request, page, number):
    dict_ = request.GET.copy()
    dict_[page] = number

    return dict_.urlencode()
