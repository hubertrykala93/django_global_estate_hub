from django.urls import path
from . import views as properties_views

urlpatterns = [
    path(route='properties', view=properties_views.properties, name='properties'),
    path(route='properties/<slug:category_slug>', view=properties_views.property_categories,
         name='property-categories'),
    path(route='properties/city/<slug:city_slug>', view=properties_views.property_cities, name='property-cities'),
    path(route='add-property', view=properties_views.add_property, name='add-property'),
    path(route='add-to-favourites', view=properties_views.add_to_favourites, name='add-to-favourites'),
    path(route='properties/<slug:category_slug>/<slug:property_slug>', view=properties_views.property_details,
         name='property-details'),
    path(route='properties/<slug:category_slug>/<slug:property_slug>/add-review', view=properties_views.add_review,
         name='add-review'),
    path(route='properties/<slug:category_slug>/<slug:property_slug>/schedule-tour',
         view=properties_views.schedule_tour, name='schedule-tour'),
    # path(route='update-filters', view=properties_views.update_filters, name='update-filters'),
]
