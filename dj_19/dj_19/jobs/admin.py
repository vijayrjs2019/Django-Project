from django.contrib import admin
from django.utils.html import format_html , mark_safe
from .models import  Jobs , ReceiveJobApplication 
# Register your models here.

def display_field(field_name, title):
    def func(self, obj):
        return getattr(obj, field_name)
    func.short_description = title
    return func

# Jobs Admin
class JobsAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'job_location','image_tag', 'is_active')
    job_title = display_field('title', 'Job Title')
    job_location = display_field('job_location', 'Job Location')
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
    
admin.site.register(Jobs, JobsAdmin)

# Jobs Application Admin
class ReceiveJobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'name', 'email', 'phone', 'resume_tag', 'created_at')
    
    def resume_tag(self, request):
        if request.resume:
            return format_html('<a href="{}" target="_blank">View Resume</a>', request.resume.url)
        return "-"
    resume_tag.short_description = 'Resume'

admin.site.register(ReceiveJobApplication, ReceiveJobApplicationAdmin)