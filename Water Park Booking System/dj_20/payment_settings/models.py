from django.db import models

# 
# Tax Info Model
# 
class TaxInfo(models.Model):
    tex_apply_type = models.CharField(max_length=50, choices=[('Flat', 'Flat'), ('Percentage', 'Percentage')], default='Percentage')
    tax_title = models.CharField(max_length=100, null=True, blank=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"TaxInfo(id={self.id}, type={self.tex_apply_type}, rate={self.tax_rate}, active={self.is_active})"
    
    class Meta:
        verbose_name = "Tax Information"
        verbose_name_plural = "Tax Informations"
    
# 
# Razorpay Settings Model
#
class RazorpaySettings(models.Model):
    gateway_mode = models.CharField(max_length=50, choices=[('Test', 'Test'), ('Live', 'Live')], default='Test')
    key_id = models.CharField(max_length=100, null=True, blank=True)
    key_secret = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"RazorpaySettings(id={self.id}, active={self.is_active})"
    
    class Meta:
        verbose_name = "Razorpay Setting"
        verbose_name_plural = "Razorpay Settings"

#
# Booking Model
#
class Booking(models.Model):
    # Booking Date
    booking_date = models.DateField(null=True, blank=True, default=None)
    #Booking Info
    Booking_id   = models.CharField(max_length=200, unique=True)
    payment_id   = models.CharField(max_length=200, null=True, blank=True)
    payment_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending')

    # User Details
    first_name  = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100)
    phone_no    = models.CharField(max_length=15)
    user_email  = models.EmailField()
    sub_total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    # Additional Info
    tax_info    = models.TextField(verbose_name='Tax Info', null=True, blank=True)
    # Package Details Snapshot
    package_title       = models.CharField(max_length=200)
    package_description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    no_person = models.IntegerField()
    # Timestamps
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking(id={self.id}, user={self.first_name} {self.last_name})"
    
    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"