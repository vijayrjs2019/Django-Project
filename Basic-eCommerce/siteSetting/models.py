from django.db import models
from django.core.exceptions import ValidationError
from tinymce.models import HTMLField
import os
import uuid
def user_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('about_us_image/', new_filename)

def testimonial_user_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('testimonial_user_image/', new_filename)

def slider_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('testimonial_user_image/', new_filename)


# Site Basic Info
class SiteSetting(models.Model):
    class Meta:
        verbose_name_plural = "Website Settings"
    site_name = models.CharField(max_length=120)
    site_email = models.EmailField()
    site_phone_no = models.CharField(max_length=15)
    site_address = models.TextField()
    facebook_link = models.TextField(null=True, blank=True)
    twitter_link = models.TextField(null=True, blank=True)
    linkedin_link = models.TextField(null=True, blank=True)
    instagram_link = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        if not self.pk and SiteSetting.objects.exists():
            raise ValidationError("Only one entry is allowed.")
        super().save(*args, **kwargs)

# About Us Info
class AboutUsInfo(models.Model):
    class Meta:
        verbose_name_plural = "About Us"
    title = models.CharField(max_length=120)
    description = HTMLField()
    image = models.FileField(upload_to=user_image_upload_path,max_length=250,null=True,default=None)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.pk and SiteSetting.objects.exists():
            raise ValidationError("Only one entry is allowed.")
        super().save(*args, **kwargs)

#Subscribe List
class SubscribeList(models.Model):
    class Meta:
        verbose_name_plural = "Subscribe List"
    email = models.CharField(max_length=120)

#Contact Us
class ContactUs(models.Model):
    class Meta:
        verbose_name_plural = "Contact Us"
    user_name = models.CharField(max_length=120)
    user_phone = models.CharField(max_length=15)
    user_email = models.CharField(max_length=120)
    user_message = models.TextField()

#Testimonial
class Testimonial(models.Model):
    class Meta:
        verbose_name_plural = "Testimonial"
    customer_name = models.CharField(max_length=120)
    customer_feedback = models.TextField()
    customer_image = models.FileField(upload_to=testimonial_user_image_upload_path,max_length=250,null=True,default=None)

#Slider List
class SliderList(models.Model):
    class Meta:
        verbose_name_plural = "Slider List"
    slide_title = models.CharField(max_length=120)
    slide_description = models.TextField()
    slide_image = models.FileField(upload_to=slider_image_upload_path,max_length=250,null=True,default=None)
    slide_buttont_ext_1 = models.CharField(max_length=120)
    slide_buttont_ext_link_1 = models.TextField(null=True, blank=True)
    slide_buttont_ext_2 = models.CharField(max_length=120)
    slide_buttont_ext_link_2 = models.TextField(null=True, blank=True)   