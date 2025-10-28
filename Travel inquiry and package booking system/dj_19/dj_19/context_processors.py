from setting.models import Setting, SocialMediaLink
from django.contrib.auth.forms import UserCreationForm
from authUsers.forms import CreateUserForm
from authUsers.models import UserProfile
def websiteInfo(request):
    data = Setting.objects.first()
    if data:
        return {
            'site_name': data.site_name,
            'site_description': data.site_description,
            'site_keywords': data.site_keywords,
            'site_logo': data.site_logo.url if data.site_logo else None, 
            'site_email': data.site_email,
            'site_hr_email': data.site_hr_email,
            'site_phone': data.site_phone,
            'site_fax': data.site_fax,
            'site_address': data.site_address,
            'site_contry': data.site_contry,
            'site_city': data.site_city,
        }
    else:
        return {
            'site_name': 'Travela',
            'site_description': '',
            'site_keywords': 'keyword1, keyword2',
            'site_logo': None,
            'site_email': '',
            'site_hr_email': '',
            'site_phone': '',
            'site_fax': '',
            'site_address': '',
            'site_contry': '',
            'site_city': '',
        }
 
def websiteDevedevelopedInfo(request):
    return {
        'devedeveloped_by': 'Vlax',
        'devedeveloped_url': 'https://vlax.in/',
    }

def websiteSocialMediaLinks(request): 
    social_links = SocialMediaLink.objects.filter(is_active=True)
    return {
        'social_links': social_links,
    }

def registrationsFormDisplay(request):
    form = CreateUserForm()
    return {
        'registrationsForm':form
    }

def userInfoByUserID(request):
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass
    return {
        'UserProfileInfo': user_profile
    }