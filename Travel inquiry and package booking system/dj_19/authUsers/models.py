from django.db import models
from django.contrib.auth.models import User
from setting.models import Countries
import os
import uuid

def user_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('user_profile_image/', new_filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_country')
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.FileField(upload_to=user_image_upload_path, max_length=250, null=True, default=None)

    def __str__(self):
        return self.user.username
