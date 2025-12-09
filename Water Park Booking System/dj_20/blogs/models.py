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

# 
# Blog Model
# 
class Blog(models.Model):
    blogCategory = models.ForeignKey('BlogCategory', on_delete=models.CASCADE,null=True, blank=True)
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False, null=True, blank=True)
    content = HTMLField(verbose_name='Blog Description')
    image = models.FileField(upload_to=facility_image_upload_path,max_length=250,null=True,default=None)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.blogCategory.name if self.blogCategory else 'No Category'})"
    
    class Meta:
        verbose_name = 'Blog List'
        verbose_name_plural = 'Blog List' 

# 
# Blog Cateogry Model
# 
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=False, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'

# 
# Blog Comment Model
#
class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user_first_name = models.CharField(max_length=100)
    user_last_name = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=100)
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user_first_name} on {self.blog.title}"
    
    class Meta:
        verbose_name = 'Blog Comment'
        verbose_name_plural = 'Blog Comments'