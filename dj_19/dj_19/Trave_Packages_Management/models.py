from django.db import models
from setting.models import Countries,Categories
from tinymce.models import HTMLField
from autoslug import AutoSlugField
from django.contrib.auth.models import User

import os
import uuid

def package_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('package_image/', new_filename)

# Travel Package
class TravelPackage(models.Model):
    HOTEL_TYPE_CHOICES = [
        ('5_star', '5 Star'),
        ('4_star', '4 Star'),
        ('3_star', '3 Star'),
        ('2_star', '2 Star'),
        ('1_star', '1 Star'),
    ]
   
    package_name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='package_name', unique=True, max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True, related_name='categories_package')
    destination = models.CharField(max_length=100)
    country = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True, blank=True, related_name='country_package')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration = models.IntegerField(help_text="Duration in days")
    no_person = models.IntegerField(help_text="No Person for the package include chldren")
    hotel_type = models.CharField(max_length=10, choices=HOTEL_TYPE_CHOICES, default='3_star')
    description = HTMLField(help_text="Enter the description of the travel package")
    thumbnail_image = models.FileField(upload_to=package_image_upload_path, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.package_name} - {self.destination}"
    
    class Meta:
        verbose_name_plural = 'Travel Package List'
        ordering = ['-created_at']

# Travel Enquiry
class TravelEnquiry(models.Model):
    HOTEL_TYPE_CHOICES = [
        ('5_star', '5 Star'),
        ('4_star', '4 Star'),
        ('3_star', '3 Star'),
        ('2_star', '2 Star'),
        ('1_star', '1 Star'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_enquiry')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_no = models.CharField(max_length=20)
    departure_date = models.DateField()
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True, related_name='categories_enquiry')
    destination = models.CharField(max_length=100)
    country = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True, blank=True, related_name='country_enquiry')
    duration = models.IntegerField(help_text="Duration in days")
    no_person = models.IntegerField(help_text="No Person for the enquiry include chldren")
    hotel_type = models.CharField(max_length=10, choices=HOTEL_TYPE_CHOICES, default='3_star')
    tourdetails = HTMLField(help_text="Enter please send your tour details")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.destination}"
    
    class Meta:
        verbose_name_plural = 'Travel Enquiry'
        ordering = ['-created_at']

# Quotation Info
class QuotationInfo(models.Model):
    travelEnquiry = models.ForeignKey(TravelEnquiry, on_delete=models.SET_NULL, null=True, blank=True, related_name='travelEnquiry_quotationInfo')
    quotation_amount= models.CharField(max_length=20) 
    quotation_deacription = HTMLField(help_text="Enter the description of the quotation")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_quotationInfo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.quotation_amount} - {self.quotation_deacription}"
    
    class Meta:
        verbose_name_plural = 'Quotation Info'
        ordering = ['-created_at']