from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
import os
import uuid

# Facility images :: Function to generate unique file path  
def facility_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('facility_images/', new_filename)

# Attractions images :: Function to generate unique file path  
def attractions_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('attractions_images/', new_filename)

# 
# ParkFacility Model
#  
class ParkFacility(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False,null=True, blank=True)
    description = HTMLField(verbose_name='Facility Description') 
    image = models.FileField(upload_to=facility_image_upload_path,max_length=250,null=True,default=None)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Facility List'
        verbose_name_plural = 'Facility List'
        ordering = ['title']  # Order by site name


# 
# park Service Model
# 
class ParkService(models.Model):
    title = models.CharField(max_length=100)
    service_icon = models.CharField(max_length=100)
    description = HTMLField(verbose_name='Service Description') 
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Service List'
        verbose_name_plural = 'Services List'
        ordering = ['title']  # Order by site name

# 
# Park Timings Model
# 
class ParkTimings(models.Model):
    day = models.CharField(max_length=150)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.day
    
    class Meta:
        verbose_name = 'Park Timing'
        verbose_name_plural = 'Park Timings'
        ordering = ['id']  # Order by id    


# 
# Park Attractions Model
#  
class ParAttractions(models.Model):
    title = models.CharField(max_length=100)
    description = HTMLField(verbose_name='Attractions Description') 
    image = models.FileField(upload_to=attractions_image_upload_path,max_length=250,null=True,default=None)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Park Attractions'
        verbose_name_plural = 'Park Attractions'
        ordering = ['title']  # Order by site name