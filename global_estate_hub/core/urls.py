from django.urls import path
from . import views as core_views

urlpatterns = [
    path(route='', view=core_views.index, name='index'),
    path(route='about', view=core_views.about, name='about'),
    path(route='faq', view=core_views.faq, name='faq'),
    path(route='contact', view=core_views.contact, name='contact'),
    path(route='newsletter', view=core_views.newsletter, name='newsletter'),
    path(route='error', view=core_views.error, name='error'),
    path(route='send-message', view=core_views.send_message, name='send-message'),
    path(route='properties-results', view=core_views.properties_results, name='properties-results'),
    path(route='top-agents', view=core_views.top_agents, name='top-agents'),
    path(route='rodo-rules', view=core_views.rodo_rules, name='rodo-rules'),
    path(route='privacy-policy', view=core_views.privacy_policy, name='privacy-policy'),
]