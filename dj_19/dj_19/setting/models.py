from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
from django.contrib.auth.models import User
import os
import uuid
def logo_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('site_logo/', new_filename)

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

def about_us_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('about_us/', new_filename)

def slider_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('slider_image/', new_filename)

def category_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('category_image/', new_filename)

def gallery_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('gallery_image/', new_filename)

# Create your models here.
class Setting(models.Model):
    site_name = models.CharField(max_length=100, verbose_name='Site Name')
    site_keywords = models.CharField(max_length=255, verbose_name='Site Keywords')
    site_email = models.EmailField(verbose_name='Site Email')
    site_hr_email = models.EmailField(verbose_name='Hr Email')
    site_phone = models.CharField(max_length=20, verbose_name='Site Phone')
    site_fax = models.CharField(max_length=20, verbose_name='Site FAX')
    site_address = models.CharField(max_length=255, verbose_name='Site Address')
    site_contry = models.CharField(max_length=255, verbose_name='Contry')
    site_city = models.CharField(max_length=255, verbose_name='City')
    site_logo = models.FileField(upload_to=logo_image_upload_path,max_length=250,null=True,default=None)
    site_description = models.TextField(verbose_name='Site Description')

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = 'Web Setting'
        verbose_name_plural = 'Website Setting'
        ordering = ['site_name']  # Order by site name

# Sosia Media Links
class SocialMediaLink(models.Model):
    social_media_title = models.CharField(max_length=50, verbose_name='Social Media Platform')
    social_media_url = models.CharField(max_length=50, verbose_name='Social Media URL')
    social_media_icon = models.CharField(max_length=50, verbose_name='Social Media icon')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.social_media_title
    
    class Meta:
        verbose_name = 'Social Media Link'
        verbose_name_plural = 'Social Media Links'
        ordering = ['social_media_title']  # Order by platform name

# About Us
class AboutUs(models.Model):
    class Meta:
        verbose_name_plural = "About Us"
    title = models.CharField(max_length=100)
    content = HTMLField()
    image = models.FileField(upload_to=about_us_upload_path, blank=True, null=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Slider Info
class Slider(models.Model):
    class Meta:
        verbose_name_plural = "Slider Setting"
        ordering = ['-created_at']
    slider_title = models.CharField(max_length=150)
    slider_sub_title =models.CharField(max_length=150)
    description = models.TextField()
    slider_button_title = models.CharField(max_length=150)
    slider_button_url = models.CharField(max_length=255)
    slider_image = models.FileField(upload_to=slider_image_upload_path, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

# Countries
class Countries(models.Model):
    class Meta:
        verbose_name_plural = 'Country List'
        ordering = ['-created_at']
    country_name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return self.country_name

# Categories
class Categories(models.Model):
    class Meta:
        verbose_name_plural = 'Category List'
        ordering = ['-created_at']
    category_name = models.CharField(max_length=100)
    category_description = models.TextField()
    category_thumbnail_image = models.FileField(upload_to=category_image_upload_path, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return self.category_name

#Our Gallery
class OurGallery(models.Model):
    class Meta:
        verbose_name_plural = 'Our Gallery'
        ordering = ['-created_at']
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_galleries', default=1, null=True, blank=True)
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True, related_name='categories_galleries')
    country = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True, blank=True, related_name='country_galleries')
    thumbnail_image = models.FileField(upload_to=gallery_image_upload_path, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    