from django import template

register = template.Library()


def replace(value):
    return value.replace('-', ' ')


register.filter(name='replace', filter_func=replace)
