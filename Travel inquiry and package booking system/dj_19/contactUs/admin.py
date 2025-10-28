from django.contrib import admin
from django.utils.html import format_html
from .models import UserEnquiry , Subscribers

# User Enquiry Admin
class UserEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'short_description','created_at', 'is_active')
    search_fields = ('name',) 
    actions = ['make_active', 'make_inactive']

    @admin.action(description="Mark selected enquiry as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected enquiry marked as Active.")

    @admin.action(description="Mark selected enquiry as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected enquiry marked as Inactive.")

    def short_description(self, obj):
        # Show first 100 characters of safe HTML
        return format_html(obj.message[:180] + '...')
    short_description.message = 'Message'

admin.site.register(UserEnquiry,UserEnquiryAdmin)

# Admin Subscribe List
class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',) 
    actions = ['make_active', 'make_inactive']

    @admin.action(description="Mark selected email as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected email marked as Active.")

    @admin.action(description="Mark selected email as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected email marked as Inactive.")

admin.site.register(Subscribers,SubscribersAdmin)