from django.contrib import admin
from .models import TaxSetting,RazorpaySetting

# Register your models here.
class TaxSettingAdmin(admin.ModelAdmin):
    list_display = ('tax_title','text_apply_type','tax_value','is_active','created_at')
    ordering = ('-created_at',)
    actions = ['make_active', 'make_inactive']

    @admin.action(description="Mark selected Tax as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected Tax marked as Active.")

    @admin.action(description="Mark selected Tax as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected Tax marked as Inactive.")

admin.site.register(TaxSetting,TaxSettingAdmin)

class RazorpaySettingAdmin(admin.ModelAdmin):
    list_display = ('gateway_mode','razorpay_key_id','razorpay_secret_key')

    def has_add_permission(self, request):
        return not RazorpaySetting.objects.exists()
    
    def has_change_permission(self, request, obj = None):
        return True

admin.site.register(RazorpaySetting,RazorpaySettingAdmin)