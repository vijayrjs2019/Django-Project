from siteSetting.models import SiteSetting
from product.models import Product 

def siteData(request):
    data = SiteSetting.objects.first()
    if data :
        site_name = data.site_name
        site_email = data.site_email
        site_phone_no = data.site_phone_no
        site_address = data.site_address
        facebook_link = data.facebook_link
        twitter_link = data.twitter_link
        linkedin_link = data.linkedin_link
        instagram_link = data.instagram_link

    else:
        site_name = 'Edgecut'
        site_email =''
        site_phone_no = ''
        site_address = ''
        facebook_link = ''
        twitter_link = ''
        linkedin_link = ''
        instagram_link = ''

    return {
        'site_name'      : site_name,
        'site_email'     : site_email,
        'site_phone_no'  : site_phone_no,
        'site_address'   : site_address,
        'facebook_link'  : facebook_link,
        'twitter_link'   : twitter_link,
        'linkedin_link'  : linkedin_link,
        'instagram_link' : instagram_link
    }

def footerData(request):
    return {
        'devedeveloped_by': 'Vlax',
        'devedeveloped_url': 'https://vlax.in/', 
    }

def footerProduct(request):
    data = Product.objects.all().order_by('-id')[:6]
    return {
        'footer_product': data,
    }
