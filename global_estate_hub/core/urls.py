from django.urls import path
from . import views as estates_views

urlpatterns = [
    path(route='', view=estates_views.index, name='index'),
    path(route='about', view=estates_views.about, name='about'),
    path(route='properties', view=estates_views.properties, name='properties'),
    path(route='faq', view=estates_views.faq, name='faq'),
    path(route='pages', view=estates_views.pages, name='pages'),
    path(route='contact', view=estates_views.contact, name='contact'),
    path(route='newsletter', view=estates_views.newsletter, name='newsletter'),
    path(route='error', view=estates_views.error, name='error'),
]
