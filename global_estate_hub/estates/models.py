from django.db import models


class Newsletter(models.Model):
    email = models.EmailField(max_length=200, unique=True, blank=False, null=True)

    class Meta:
        verbose_name_plural = 'Newsletters'

    def __str__(self):
        return self.email
