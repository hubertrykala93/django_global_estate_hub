from django.db import models
from django.utils.timezone import now


class Newsletter(models.Model):
    subscribed_at = models.DateTimeField(default=now)
    email = models.EmailField(max_length=200, unique=True, blank=False, null=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Newsletters'
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email
