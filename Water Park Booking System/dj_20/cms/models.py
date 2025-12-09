from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField  
import os
import uuid

# Facility images :: Function to generate unique file path  
def cms_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('facility_images/', new_filename)

# Create your models here.
class CMS(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False, null=True, blank=True)
    content = HTMLField(verbose_name='CMS Content')
    image = models.FileField(upload_to=cms_image_upload_path,max_length=250,null=True,blank=True,default=None)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Content List'
        verbose_name_plural = 'Content List' 