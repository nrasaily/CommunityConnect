from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    VISIBILITY_CHOICES = [
        ("private", "Private"),
        ("members", "Members Only"),
        ("public", "Public"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone_visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default="private")
    email_visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default="private")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return self.user.username
