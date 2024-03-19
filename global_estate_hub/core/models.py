from django.db import models
from django.utils.timezone import now


class Newsletter(models.Model):
    """
    Creating Newsletter model instance.
    """
    id = models.AutoField(primary_key=True, editable=False)
    subscribed_at = models.DateTimeField(default=now, editable=False)
    email = models.EmailField(max_length=200, unique=True, null=True)

    class Meta:
        verbose_name_plural = 'Newsletters'
        ordering = ['-subscribed_at']

    def __str__(self) -> str:
        """
        Returns the string representation of the user's email address and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return self.email


class ContactMail(models.Model):
    """
    Creating ContactMail model instance.
    """
    id = models.AutoField(primary_key=True, editable=False)
    date_sent = models.DateTimeField(default=now, editable=False)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    content = models.TextField(max_length=2000)

    class Meta:
        verbose_name_plural = 'Contact Mails'
        ordering = ['-date_sent']

    def __str__(self) -> str:
        """
        Returns the string representation of the user's full name and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return f'E-mail from {self.full_name}.'
