from django.db import models

# Create your models here.
class TaxSetting(models.Model):
    class Meta:
        verbose_name = "Tax Setting"
        verbose_name_plural = "Tax Setting"  # Correct plural
    text_apply_type = models.CharField(max_length=50, choices=[('Flat', 'Flat'), ('Percentage', 'Percentage')], default='Percentage')
    tax_title = models.CharField(max_length=256,null=True, blank=True)
    tax_value = models.CharField(max_length=256,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.text_apply_type} ({self.tax_value}%)"
    
class RazorpaySetting(models.Model):
    class Meta:
        verbose_name_plural = "Razorpay Gateway Setting"  # Correct plural
    gateway_mode = models.CharField(max_length=50, choices=[('Test', 'Test'), ('Live', 'Live')], default='Test')
    razorpay_key_id = models.CharField(max_length=250)
    razorpay_secret_key = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)