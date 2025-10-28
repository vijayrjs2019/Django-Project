from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField

import os,uuid


def jobs_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('jobs_image/', new_filename)

def job_applications_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('job_applications/', new_filename)


# Create your models here.
class Jobs(models.Model):
    class Meta:
        verbose_name_plural = "Jobs List"
    title = models.CharField(max_length=100)
    job_location = models.CharField(max_length=100)
    content = HTMLField()
    image = models.FileField(upload_to=jobs_upload_path, blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class ReceiveJobApplication(models.Model):
    class Meta:
        verbose_name_plural = "Job Applications"
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    content = HTMLField(blank=True, null=True)
    resume = models.FileField(upload_to=job_applications_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
