from django.contrib import admin
from django.utils.html import format_html
from .models import TravelGuide,Testimonial,OurServices
# Register your models here.
class TravelGuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag', 'phone_no', 'address', 'email', 'created_at','is_active')
    search_fields = ('name', 'address', 'email')
    actions = ['make_active', 'make_inactive']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;"/>', obj.image.url)
        return "No Image"
    image_tag.short_description = 'Image' 

    @admin.action(description="Mark selected guide as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected guide marked as Active.")

    @admin.action(description="Mark selected guide as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected guide marked as Inactive.")

admin.site.register(TravelGuide, TravelGuideAdmin)

# Admin Testimonial
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag', 'country', 'rating', 'short_message', 'created_at','is_active')
    search_fields = ('name', 'country', 'country')
    actions = ['make_active', 'make_inactive']

    def image_tag(self, obj):
        if obj.user_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;"/>', obj.user_image.url)
        return "No Image"
    image_tag.short_description = 'Image' 

    @admin.action(description="Mark selected Testimonial as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected Testimonial marked as Active.")

    @admin.action(description="Mark selected Testimonial as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected Testimonial marked as Inactive.")
    
    def short_message(self, obj):
        # Show first 100 characters of safe HTML
        return format_html(obj.message[:200] + '...')
    short_message.short_message = 'Message'

admin.site.register(Testimonial,TestimonialAdmin)

# Our Services Admin
class OurServicesAdmin(admin.ModelAdmin):
    list_display = ('title','image_tag','short_description', 'is_active')
    actions = ['make_active', 'make_inactive'] 

    def image_tag(self,request):
        if request.image:
            return format_html('<img src="{}" width="50" height="50" />',request.image.url)
        return "-"
    image_tag.short_description = 'Image' 

    @admin.action(description="Mark selected links as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected links marked as Active.")

    @admin.action(description="Mark selected links as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected links marked as Inactive.")

    def short_description(self, obj):
        # Show first 100 characters of safe HTML
        return format_html(obj.discription[:200] + '...')
    short_description.short_description = 'Description'
    
admin.site.register(OurServices, OurServicesAdmin)