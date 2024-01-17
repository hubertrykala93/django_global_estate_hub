from django.urls import path
from . import views as properties_views

urlpatterns = [
    path(route='properties', view=properties_views.properties, name='properties'),
    path(route='update-filters', view=properties_views.update_filters, name='update-filters'),
    path(route='properties/property-results', view=properties_views.property_results, name='property-results'),
    path(route='add-property', view=properties_views.add_property, name='add-property'),
    path(route='add-to-favourites', view=properties_views.add_to_favourites, name='add-to-favourites'),
    path(route='properties/<slug:property_slug>', view=properties_views.property_details, name='property-details'),
]
