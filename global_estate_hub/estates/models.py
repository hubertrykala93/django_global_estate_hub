from django.db import models


class Newsletter(models.Model):
    email = models.EmailField(max_length=200, blank=True, null=True)
