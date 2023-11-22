from django.db import models
from django.utils.timezone import now


class Newsletter(models.Model):
    subscribed_at = models.DateTimeField(default=now)
    email = models.EmailField(max_length=200, unique=True, null=True)

    class Meta:
        verbose_name_plural = 'Newsletters'
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class ContactMail(models.Model):
    date_sent = models.DateTimeField(default=now)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    message = models.TextField(max_length=2000)

    class Meta:
        verbose_name_plural = 'Contact Form Mails'
        ordering = ['-date_sent']

    def __str__(self):
        return f'E-mail from {self.full_name}.'
