from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.utils.timezone import now, timedelta
from PIL import Image
import os


class CustomUserManager(UserManager):
    """
    Creating custom User Manager model.
    """

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('You have not provided a valid e-mail address.')

        email = self.normalize_email(email=email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(raw_password=password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username=username, email=email, password=password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username=username, email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Creating custom User model instance.
    """
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    image = models.ImageField(default='default_profile_image.jpg', upload_to='profile_images')
    is_individual = models.BooleanField(default=True)
    is_business = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=now)
    last_login = models.DateTimeField(null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        """
        Returns the string representation of the user's username and displays it in the administrator panel.

        return: str
        """
        return self.username

    def save(self, *args, **kwargs):
        """
        Converts the user's profile image to a smaller size of 300 x 300.

        return: None
        """
        super(User, self).save(*args, **kwargs)

        img = Image.open(fp=self.image.path)

        if img.mode == 'RGBA':
            img.convert(mode='RGB')

        if img.width > 300 or img.height > 300:
            img.thumbnail(size=(300, 300))
            img.save(fp=self.image.path)


class OneTimePasswordManager(models.Manager):
    """
    Creating OneTimePasswordManager model.
    """

    def get_queryset(self):
        """
        Automatically deletes the OneTimePassword after 5 minutes.
        """
        return super().get_queryset().filter(created_at__gte=now() - timedelta(minutes=5))


class OneTimePassword(models.Model):
    """
    Creating OneTimePassword model instance.
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=now)
    expires_in = models.DateTimeField(default=now() + timedelta(minutes=5))
    objects = OneTimePasswordManager()

    class Meta:
        verbose_name = 'One Time Password'
        verbose_name_plural = 'One Time Passwords'

    def __str__(self):
        """
        Returns the string representation of the username of the user
        to whom the OneTimePassword has been assigned and displays it in the administrator panel.

        return: str
        """
        return f'One Time Password for {self.user.username}.'


class Individual(models.Model):
    """
    Creating IndividualProfile model instance.
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=(
        ('Not Defined', 'Not Defined'),
        ('Male', 'Male'),
        ('Female', 'Female')
    ), blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    website_url = models.URLField(max_length=200, null=True, blank=True)
    facebook_url = models.URLField(max_length=200, null=True, blank=True)
    instagram_url = models.URLField(max_length=200, null=True, blank=True)
    linkedin_url = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Individual Profile'
        verbose_name_plural = 'Individual Profiles'

    def __str__(self):
        """
        Returns the string representation of the profile's username and displays it in the administrator panel.

        return: str
        """
        return f'{self.user.username} Individual Profile.'


class Business(models.Model):
    """
    Creating BusinessProfile model instance.
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, null=True)
    company_id = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=150, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    website_url = models.URLField(max_length=200, null=True, blank=True)
    facebook_url = models.URLField(max_length=200, null=True, blank=True)
    instagram_url = models.URLField(max_length=200, null=True, blank=True)
    linkedin_url = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Business Profile'
        verbose_name_plural = 'Business Profiles'

    def __str__(self):
        """
        Returns the string representation of the business's name and displays it in the administrator panel.

        return: str
        """
        return f'{self.company_name} Business Profile.'
