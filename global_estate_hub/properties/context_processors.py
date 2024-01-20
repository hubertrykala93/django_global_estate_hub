from .models import Property


def featured_properties(request):
    return {
        "featured_properties": Property.objects.filter(is_featured=True)
    }
