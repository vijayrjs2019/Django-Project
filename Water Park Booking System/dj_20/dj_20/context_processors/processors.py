from website_setting.models import SiteInfo , SocialMediaLinks , Testimonial , TeamMember
from park_facilities.models import ParkTimings
from packages.models import Package
# Context Processors
# These functions will be used to pass data to all templates
# They must return a dictionary
# Add your context processors here

# Website Information Context Processor
def websiteInfo(request):
    data = SiteInfo.objects.first()
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
            'site_name': 'WaterLand',
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
 
# Website Developed By Context Processor
def websiteDevedevelopedInfo(request):
    return {
        'devedeveloped_by': 'Vlax',
        'devedeveloped_url': 'https://vlax.in/',
    }

# Social Media Links Context Processor
def showSocialMediaLinks(request):
    data = SocialMediaLinks.objects.first()
    if data:
        return {
            'facebook_url': data.facebook_url,
            'x_url': data.x_url,
            'instagram_url': data.instagram_url,
            'linkedIn_url': data.linkedIn_url,
        }
    else:
        return {
            'facebook_url': '',
            'x_url': '',
            'instagram_url': '',
            'linkedIn_url': '',
        }
    
# Testimonials Context Processor
def showTestimonials(request):
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-id')[:3]
    return {
        'testimonials': testimonials
    }

# Team Members Context Processor
def showTeamMembers(request):
    team_members = TeamMember.objects.filter(is_active=True).order_by('id')
    return {
        'team_members': team_members
    }   

# Opening Hours Context Processor
def getOpeningHours(request):
    openingHours = ParkTimings.objects.filter(is_active=True)
    return {
        'openingHours':openingHours
    }
    
# Packages Context Processor
def getActivePackages(request):
    packages = Package.objects.filter(is_active=True).order_by('price')
    return {
        'packages': packages
    }