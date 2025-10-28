from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
# Create your models here.
import os
import uuid

def user_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('blogs_image/', new_filename)

class Blog(models.Model):
    class Meta:
        verbose_name_plural = "Blog List"
    title = models.CharField(max_length=100)
    content = HTMLField()
    image = models.FileField(upload_to=user_image_upload_path, blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class BlogComment(models.Model):
    class Meta:
        verbose_name_plural = "Blog Comments"
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.blog.title}"