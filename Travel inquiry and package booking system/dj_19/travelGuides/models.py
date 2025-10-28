from django.db import models
import os
import uuid
from tinymce.models import HTMLField
from autoslug import AutoSlugField

def user_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('travel_guide_image/', new_filename)

def testimonial_user_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('testimonial_user_image/', new_filename)

def our_services_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('our_services_image/', new_filename)

# Create your models here.
class TravelGuide(models.Model):
    name = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, blank=True, null=True)
    description = models.TextField()
    image = models.FileField(upload_to=user_image_upload_path, blank=True, null=True)
    facebook_link = models.URLField(max_length=200, blank=True, null=True)
    instagram_link = models.URLField(max_length=200, blank=True, null=True)
    twitter_link = models.URLField(max_length=200, blank=True, null=True)
    youtube_link = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Travel Guides"
        ordering = ['-created_at']

# Testimonial
class Testimonial(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    user_image = models.FileField(upload_to=testimonial_user_image_upload_path, blank=True, null=True)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES,default=1)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.country}) - {self.rating}★"
    
# Our Services
class OurServices(models.Model):
    class Meta:
        verbose_name_plural = 'Our Services' #verbose_name_plural
        ordering = ['-created_at']
    title = models.CharField(max_length=100)
    discription = HTMLField()
    image = models.FileField(upload_to=our_services_image_upload_path, blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
