from django.db import models 
from Trave_Packages_Management.models import QuotationInfo,TravelPackage,TravelEnquiry
from django.contrib.auth.models import User
from setting.models import Countries,Categories
from tinymce.models import HTMLField

class BookingList(models.Model):
    HOTEL_TYPE_CHOICES = [
        ('5_star', '5 Star'),
        ('4_star', '4 Star'),
        ('3_star', '3 Star'),
        ('2_star', '2 Star'),
        ('1_star', '1 Star'),
    ]

    booking_type = models.CharField(
        max_length=50,
        choices=[('Quotation', 'Quotation'), ('Package', 'Package')],
        default='Quotation'
    )
    # User Information
    TravelEnquiry = models.ForeignKey(TravelEnquiry, on_delete=models.SET_NULL, null=True, blank=True, related_name='booking_TravelEnquiry')
    quotationInfo = models.ForeignKey(QuotationInfo, on_delete=models.SET_NULL, null=True, blank=True, related_name='booking_quotationInfo')
    travelPackage = models.ForeignKey(TravelPackage, on_delete=models.SET_NULL, null=True, blank=True, related_name='booking_travelPackage')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='booking_users')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_no = models.CharField(max_length=20)
    departure_date = models.DateField()
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True, related_name='booking_categories')
    destination = models.CharField(max_length=100)
    country = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True, blank=True, related_name='booking_country')
    duration = models.IntegerField(help_text="Duration in days")
    no_person = models.IntegerField(help_text="No Person for the enquiry include chldren")
    hotel_type = models.CharField(max_length=10, choices=HOTEL_TYPE_CHOICES, default='3_star')
    tourdetails = HTMLField(help_text="Enter please send your tour details")
    # Billing Information
    order_id = models.CharField(max_length=255, null=True, blank=True)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default="0.00")
    sub_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default="0.00")
    other_charges_amount = models.DecimalField(max_digits=10, decimal_places=2, default="0.00")
    other_charges_info = models.TextField(blank=True, null=True)
    payment_status = models.TextField(blank=True, null=True)
    payment_status = models.CharField(
        max_length=50,
        choices=[('failed', 'failed'), ('pending', 'pending'), ('success', 'success')],
        default='pending'
    )
    #  Update Information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True) 
