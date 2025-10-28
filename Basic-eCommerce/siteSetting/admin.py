from django.contrib import admin
from .models import SiteSetting ,AboutUsInfo,SubscribeList,ContactUs,Testimonial,SliderList
from django.utils.html import format_html , strip_tags

# Site Setting
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name','site_email','site_phone_no','site_address','facebook_link','twitter_link','linkedin_link','instagram_link')

    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()
    
    def has_change_permission(self, request, obj = None):
        return True
    
admin.site.register(SiteSetting,SiteSettingAdmin)

# About Us
class AboutUsInfoAdmin(admin.ModelAdmin):
    list_display = ('title','clean_description','image_tag')

    def has_add_permission(self, request):
        return not AboutUsInfo.objects.exists()
    
    def has_change_permission(self, request, obj = None):
        return True
    
    def image_tag(self,request):
        if request.image:
            return format_html('<img src="{}" width="50" height="50" />',request.image.url)
        return "-"
    image_tag.short_description = 'Image'

    def clean_description(self, obj):
        if obj.description:
            return strip_tags(obj.description)
        return "-"
    clean_description.short_description = 'Description'

admin.site.register(AboutUsInfo,AboutUsInfoAdmin)

#Subscribe List
class SubscribeListAdmin(admin.ModelAdmin):
    list_display = ('email',)

    def has_add_permission(self, request):
        return False  # Disables the "Add" button

    def has_change_permission(self, request, obj=None):
        return False  # Disables the edit option

admin.site.register(SubscribeList,SubscribeListAdmin)

#Contact Us
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('user_name','user_phone','user_email','user_message')

    def has_add_permission(self, request):
        return False  # Disables the "Add" button

    def has_change_permission(self, request, obj=None):
        return False  # Disables the edit option

admin.site.register(ContactUs,ContactUsAdmin)

# Testimonial
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name','user_image_tag','customer_feedback')

    def user_image_tag(self,request):
        if request.customer_image:
            return format_html('<img src="{}" width="50" height="50" />',request.customer_image.url)
        return "-"
    user_image_tag.short_description = 'User Image'

admin.site.register(Testimonial,TestimonialAdmin)

# Slider List
class   SliderListAdmin(admin.ModelAdmin):
    list_display = ('slide_title','slider_Image_tag','slide_description','slide_button_1_tag','slide_button_2_tag',)
    
    def slider_Image_tag(self,request):
        if request.slide_image:
            return format_html('<img src="{}" width="50" height="50" />',request.slide_image.url)
        return "-"
    slider_Image_tag.short_description = 'Slider Image'

    def slide_button_1_tag(self, obj):
        if obj.slide_buttont_ext_link_1:
            return format_html(
                '<a href="{}" target="_blank">{}</a>',
                obj.slide_buttont_ext_link_1,
                obj.slide_buttont_ext_1
            )
        return obj.slide_buttont_ext_1
    slide_button_1_tag.short_description = 'Button Text 1'

    def slide_button_2_tag(self, obj):
        if obj.slide_buttont_ext_link_2:
            return format_html(
                '<a href="{}" target="_blank">{}</a>',
                obj.slide_buttont_ext_link_2,
                obj.slide_buttont_ext_2
            )
        return obj.slide_buttont_ext_2
    slide_button_2_tag.short_description = 'Button Text 2'

admin.site.register(SliderList,SliderListAdmin)


