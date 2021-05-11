from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from user.constants.languages import SUPPORTED_LANGUAGES


class User(AbstractUser):
    first_name = None
    last_name = None
    username = None
    name = models.CharField(max_length=244,
                            help_text="Full name of user.")
    email = models.EmailField(unique=True)

    identity_document = models.FileField(help_text="Image of a valid Id Card.")
    profile_photo = models.ImageField(blank=True, null=True, help_text="Profile Picture of user.")
    verification_status = models.BooleanField(default=False)
    user_role = models.CharField(max_length=1, blank=True)
    phone_number = models.CharField(max_length=15)
    referral_code = models.CharField(max_length=8, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=5, choices=SUPPORTED_LANGUAGES)

    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-last_updated']





class Referral(models.Model):
    referred_by = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='referred_by')
    referred_to = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='referred_to')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.referred_to.email


class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=2, )  # todo choice field
    is_ack = models.BooleanField(default=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class ForgetPasswordToken(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    expire_at = models.DateTimeField()
    token = models.CharField(max_length=10)

    @property
    def is_expired(self):
        return self.expire_at >= timezone.now()
