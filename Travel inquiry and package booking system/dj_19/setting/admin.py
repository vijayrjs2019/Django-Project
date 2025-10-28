from django.contrib import admin
from django.utils.html import format_html , mark_safe
from .models import Setting, SocialMediaLink , AboutUs ,Slider , Countries ,Categories ,OurGallery
from django.contrib.auth.models import User

# Register your models here.
def display_field(field_name, title):
    def func(self, obj):
        return getattr(obj, field_name)
    func.short_description = title
    return func

class SettingAdmin(admin.ModelAdmin):
    list_display = (
        'site_name_display', 'site_email_display','site_hr_email', 'site_phone_display',
        'site_fax_display', 'site_address_display','site_contry','site_city', 'image_tag'
    )

    site_name_display = display_field('site_name', 'Company Name')
    site_email_display = display_field('site_email', 'Email')
    site_hr_email_display = display_field('site_hr_email', 'HR Email')
    site_phone_display = display_field('site_phone', 'Phone')
    site_fax_display = display_field('site_fax', 'Fax No')
    site_address_display = display_field('site_address', 'Company Address')
    site_contry_display = display_field('site_contry', 'Contry')
    site_city_display = display_field('site_city', 'City')
    
    

    def image_tag(self,request):
        if request.site_logo:
            return format_html('<img src="{}" width="50" height="50" />',request.site_logo.url)
        return "-"
    image_tag.short_description = 'Logo'   

    def has_add_permission(self, request):
        return False  # disables adding new settings

    def has_delete_permission(self, request, obj=None):
        return False  # disables deleting settings 
admin.site.register(Setting, SettingAdmin)

# Sosia Media Links 
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('social_media_title', 'social_media_url', 'social_media_icon','is_active')
    actions = ['make_active', 'make_inactive'] 

    @admin.action(description="Mark selected links as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected links marked as Active.")

    @admin.action(description="Mark selected links as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected links marked as Inactive.")

admin.site.register(SocialMediaLink, SocialMediaLinkAdmin)

#  About Us Admin
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'safe_content', 'image_tag')

    def safe_content(self, obj):
        return mark_safe(obj.content)  # Safely render HTML in admin list
    safe_content.short_description = 'Content'

    def image_tag(self, request):
        if request.image:
            return format_html('<img src="{}" width="50" height="50" />', request.image.url)
        return "-"
    image_tag.short_description = 'Image'

    def has_add_permission(self, request):
        # Allow add only if no AboutUs entries exist
        return not AboutUs.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False  # Disable delete

admin.site.register(AboutUs, AboutUsAdmin)

# Slider Info Admin
class SliderAdmin(admin.ModelAdmin):
    list_display = ('slider_title','image_tag','slider_sub_title','short_message','is_active')
    search_fields = ('slider_title', 'slider_sub_title')
    actions = ['make_active', 'make_inactive']

    def image_tag(self, obj):
        if obj.slider_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;"/>', obj.slider_image.url)
        return "No Image"
    image_tag.short_description = 'Slider Image' 

    @admin.action(description="Mark selected Slider as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected Slider marked as Active.")

    @admin.action(description="Mark selected Slider as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected Slider marked as Inactive.")
    
    def short_message(self, obj):
        # Show first 100 characters of safe HTML
        return format_html(obj.description[:200] + '...')
    short_message.short_message = 'Description'

admin.site.register(Slider,SliderAdmin)

# Countries Admin
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('country_name','created_at','is_active')
    search_fields = ('country_name',)
    actions = ['make_active', 'make_inactive']

    @admin.action(description="Mark selected country as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected country marked as Active.")

    @admin.action(description="Mark selected country as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected country marked as Inactive.")


admin.site.register(Countries,CountriesAdmin)

# Categories Admin
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category_name','image_tag','short_message','created_at','is_active')
    search_fields = ('category_name',)
    actions = ['make_active', 'make_inactive']

    def image_tag(self, obj):
        if obj.category_thumbnail_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;"/>', obj.category_thumbnail_image.url)
        return "No Image"
    image_tag.short_description = 'Thumbnail' 

    @admin.action(description="Mark selected category as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected category marked as Active.")

    @admin.action(description="Mark selected category as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected category marked as Inactive.")
    
    def short_message(self, obj):
        # Show first 100 characters of safe HTML
        return format_html(obj.category_description[:200] + '...')
    short_message.short_message = 'Description'

    def __str__(self):
        return self.category_name

admin.site.register(Categories,CategoriesAdmin)

# Our Gallery Admin
class OurGalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag', 'user_name_display', 'category', 'country', 'created_at', 'is_active')
    search_fields = ('title',)
    actions = ['make_active', 'make_inactive'] 

    def image_tag(self, obj):
        if obj.thumbnail_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;"/>', obj.thumbnail_image.url)
        return "No Image"
    image_tag.short_description = 'Thumbnail'

    def user_name_display(self, obj):
        # Show admin name if user is None or user.id == 1
        if not obj.user or obj.user.id == 1:
            try:
                admin_user = User.objects.get(id=1)
                return admin_user.get_full_name() or admin_user.username
            except User.DoesNotExist:
                return "Admin"
        return obj.user.get_full_name() or obj.user.username
    user_name_display.short_description = "User"

    @admin.action(description="Mark selected display image as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected display image marked as Active.")

    @admin.action(description="Mark selected display image as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected display image marked as Inactive.")

admin.site.register(OurGallery, OurGalleryAdmin)
