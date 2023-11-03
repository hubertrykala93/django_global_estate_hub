from django import template

register = template.Library()


def replace(value):
    return value.replace('-', ' ')


def length(value):
    return len(value)


register.filter(name='replace', filter_func=replace)
