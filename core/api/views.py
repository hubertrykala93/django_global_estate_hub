from .serializers import NewsletterSerializer
from core.models import Newsletter
from rest_framework.generics import ListAPIView


class NewsletterAPIView(ListAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def get_view_name(self):
        return "Global Estate Hub Newsletters"

    def get_view_description(self, html=False):
        return "API view with all newsletters on the Global Estate Hub platform."
