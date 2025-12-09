from django.contrib import admin
from .models import TaxInfo , RazorpaySettings , Booking

# 
#   TaxInfo Admin Configuration 
# 
class TaxInfoAdmin(admin.ModelAdmin):
    list_display = ('tax_title', 'tex_apply_type', 'tax_rate', 'is_active', 'created_at', 'updated_at')
    search_fields = ('tex_apply_type',)
    ordering = ('-id',)
    readonly_fields = ('created_at', 'updated_at')

    actions = ['make_active', 'make_inactive']

    @admin.action(description='Activate selected')
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} tax record(s) activated successfully.", level='success')
    
    @admin.action(description='Deactivate selected')
    def make_inactive(self, request, queryset):
        updated= queryset.update(is_active=False)
        self.message_user(request, f"{updated} tax record(s) deactivated successfully.", level='warning')

admin.site.register(TaxInfo, TaxInfoAdmin)

# 
#   RazorpaySettings Admin Configuration
#
class RazorpaySettingsAdmin(admin.ModelAdmin):
    list_display = ('gateway_mode', 'key_id', 'is_active', 'created_at', 'updated_at')
    search_fields = ('gateway_mode',)
    ordering = ('-id',)
    readonly_fields = ('created_at', 'updated_at')

    actions = ['make_active', 'make_inactive']

    @admin.action(description='Activate selected')
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} Razorpay setting(s) activated successfully.", level='success')
    
    @admin.action(description='Deactivate selected')
    def make_inactive(self, request, queryset):
        updated= queryset.update(is_active=False)
        self.message_user(request, f"{updated} Razorpay setting(s) deactivated successfully.", level='warning')

    # hide add button if record already exists
    def has_add_permission(self, request):
        if RazorpaySettings.objects.count() >= 1:   # allow only one entry
            return False
        return True

    # still allow edit
    def has_change_permission(self, request, obj=None):
        return True

admin.site.register(RazorpaySettings, RazorpaySettingsAdmin)

# 
#   Booking Admin Configuration
#
class BookingAdmin(admin.ModelAdmin):
    list_display = ('Booking_id','booking_date', 'first_name','phone_no', 'user_email', 'last_name','payment_id','payment_status', 'total_price', 'created_at')
    search_fields = ('Booking_id','booking_date','payment_id', 'payment_status')
    ordering = ('-id',)

     # hide add button if record already exists
    def has_add_permission(self, request):
        if RazorpaySettings.objects.count() >= 1:   # allow only one entry
            return False
        return True
    
    # still allow edit
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Booking, BookingAdmin)