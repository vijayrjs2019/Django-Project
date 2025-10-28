from django.contrib import admin
from .models import Category,Product,ProductDelivery,TaxSetting,ShippingCostSetting,RazorpaySetting
from django.utils.html import format_html

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name','slug')

admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_tag','product_name','category','product_price','created_at')

    def image_tag(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.product_image.url)
        return "-"
    image_tag.short_description = 'Image' 

admin.site.register(Product,ProductAdmin)

class ProductDeliveryAdmin(admin.ModelAdmin):
    list_display = ('order_id','product','product_price','shipping_type','shipping_cost','tax_apply_type','tax_value','tax_apply','total_price','first_name','last_name','email','phone_no','country','state','city','zip_code','delivery_address','payment_status','payment_method','delivery_status','created_at')
    
    # Make all fields readonly except delivery_status
    readonly_fields = (
        'payment_method','payment_status','total_price','order_id','product','product_price','shipping_type','shipping_cost','tax_apply_type','tax_value','tax_apply','first_name', 'last_name','email', 'phone_no', 'country',
        'state', 'city', 'zip_code', 'delivery_address', 'created_at'
    )

    # Optional: limit which fields show in the form
    fields = (
        'delivery_status',
        *readonly_fields  # ensures they still display in the form
    )
    

admin.site.register(ProductDelivery,ProductDeliveryAdmin)

class TaxSettingAdmin(admin.ModelAdmin):
    list_display = ('text_apply_type','tax_value')

    def has_add_permission(self, request):
        return not TaxSetting.objects.exists()
    
    def has_change_permission(self, request, obj = None):
        return True

admin.site.register(TaxSetting,TaxSettingAdmin)

class ShippingCostSettingAdmin(admin.ModelAdmin):
    list_display = ('cost_apply_type','cost_value')

    def has_add_permission(self, request):
        return not ShippingCostSetting.objects.exists()
    
    def has_change_permission(self, request, obj = None):
        return True

admin.site.register(ShippingCostSetting,ShippingCostSettingAdmin)

class RazorpaySettingAdmin(admin.ModelAdmin):
    list_display = ('gateway_mode','razorpay_key_id','razorpay_secret_key')

    def has_add_permission(self, request):
        return not RazorpaySetting.objects.exists()
    
    def has_change_permission(self, request, obj = None):
        return True

admin.site.register(RazorpaySetting,RazorpaySettingAdmin)