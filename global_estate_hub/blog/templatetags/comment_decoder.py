from django import template
import urllib.parse
import requests

register = template.Library()


# @register.filter(name='decode_comment')
# def decode_comment(value):
#     print(requests.utils.unquote(string=value))
#     return requests.utils.unquote(string=value).lstrip()
