from django.db import models
from autoslug import AutoSlugField
from tinymce.models import HTMLField
import os
import uuid
from django.core.exceptions import ValidationError

#Category
class Category(models.Model):
    class Meta:
        verbose_name_plural = "Category List"
    category_name = models.CharField(max_length=256)
    slug = AutoSlugField(populate_from='category_name',unique=True,null=True)

    def __str__(self):
         return self.category_name

def user_image_upload_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return new file path
    return os.path.join('product_image/', new_filename)

#Product 
class Product(models.Model):
    class Meta:
        verbose_name_plural = "Product List"
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=False)
    product_name = models.CharField(max_length=256)
    product_price = models.IntegerField(max_length=100)
    product_discription  = HTMLField()
    product_image = models.FileField(upload_to=user_image_upload_path,max_length=256,null=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from='product_name',unique=True,null=True)

    def __str__(self):
            return f"{self.product_name} ({self.category.category_name if self.category else 'No Category'})"

class ProductDelivery(models.Model):
    class Meta:
        verbose_name = "Order List"
        verbose_name_plural = "Order List"  # Correct plural
    order_id = models.CharField(max_length=256,unique=True,null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_price = models.CharField(max_length=256,null=True, blank=True)
    shipping_type = models.CharField(max_length=256,null=True, blank=True)
    shipping_cost = models.CharField(max_length=256,null=True, blank=True)
    tax_apply_type = models.CharField(max_length=256,null=True, blank=True)
    tax_value = models.CharField(max_length=256,null=True, blank=True)
    tax_apply = models.CharField(max_length=256,null=True, blank=True)
    total_price = models.CharField(max_length=256,null=True, blank=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(max_length=256,null=True, blank=True)
    phone_no = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    zip_code = models.CharField(max_length=256)
    delivery_address = models.CharField(max_length=256)
    delivery_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Delivered', 'Delivered')], default='Pending')
    payment_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Failed', 'Failed')], default='Pending')
    payment_method = models.CharField(max_length=50, choices=[('Cash On Delivery', 'Cash On Delivery'), ('Razorpay', 'Razorpay')], default='Razorpay')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery for {self.product.product_name}"
    
class TaxSetting(models.Model):
    class Meta:
        verbose_name = "Tax Setting"
        verbose_name_plural = "Tax Setting"  # Correct plural
    text_apply_type = models.CharField(max_length=50, choices=[('Flat', 'Flat'), ('Percentage', 'Percentage')], default='Percentage')
    tax_value = models.CharField(max_length=256,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text_apply_type} ({self.tax_value}%)"
    
class ShippingCostSetting(models.Model):
    class Meta:
        verbose_name_plural = "Shipping Cost Setting"  # Correct plural
    
    cost_apply_type = models.CharField(max_length=50, choices=[('Free', 'Free'), ('Paid', 'Paid')], default='Free')
    
    # Changed to IntegerField to better represent the cost value as a number
    cost_value = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Validation: If cost_apply_type is 'Paid', cost_value should be greater than 1
        if self.cost_apply_type == 'Paid' and (self.cost_value is None or self.cost_value <= 1):
            raise ValidationError({'cost_value': 'Cost value must be greater than 1 when the cost type is Paid.'})
        
        # Validation: If cost_apply_type is 'Paid', cost_value is required
        if self.cost_apply_type == 'Paid' and self.cost_value is None:
            raise ValidationError({'cost_value': 'Cost value is required when cost type is Paid.'})
        
        # Validation: If cost_apply_type is 'Free', cost_value must be 0
        if self.cost_apply_type == 'Free' and (self.cost_value is None or self.cost_value > 0):
            raise ValidationError({'cost_value': 'Cost value must be 0 when the cost type is Free.'})
    
    def save(self, *args, **kwargs):
        # If the cost_apply_type is 'Free' and cost_value is not set, set it to 0
        if self.cost_apply_type == 'Free' and self.cost_value is None:
            self.cost_value = 0  # Set it as an integer (0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cost_apply_type} ({self.cost_value}%)"
    
class RazorpaySetting(models.Model):
    class Meta:
        verbose_name_plural = "Razorpay Setting"  # Correct plural
    gateway_mode = models.CharField(max_length=50, choices=[('Test', 'Test'), ('Live', 'Live')], default='Test')
    razorpay_key_id = models.CharField(max_length=250)
    razorpay_secret_key = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)