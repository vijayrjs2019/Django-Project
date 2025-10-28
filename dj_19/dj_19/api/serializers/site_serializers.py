from rest_framework import serializers
from django.utils.html import strip_tags
from setting.models import Setting , SocialMediaLink , AboutUs , Slider ,OurGallery , Categories ,Countries
from cms.models import CMS
from travelGuides.models import Testimonial , OurServices ,TravelGuide

# Site information serializers
class SiteSettingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = '__all__'

# All Site Social Media Link
class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = '__all__'

# Site About us info
class AboutUsSerializer(serializers.ModelSerializer):
    content  = serializers.SerializerMethodField()

    class Meta:
        model = AboutUs
        fields = ['id', 'title', 'content','image']
    
    def get_content(self, obj):
        return strip_tags(obj.content) 

# Slider List
class SliderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'

# Gallery List
class GalleryListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    contry_name = serializers.CharField(source='country.country_name', read_only=True)
    class Meta:
        model = OurGallery
        fields = '__all__'

    def get_category_name(self, obj):
        return obj.category.id if obj.category else None
    
    def get_country_name(self, obj):
        return obj.country.id if obj.country else None

# category List
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

# Country List
class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = '__all__'

#CMS Content
class CMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMS
        fields = '__all__'

# Testimonial
class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

# Services
class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurServices
        fields = '__all__'

# Travel Guides
class TravelGuidesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelGuide
        fields = '__all__'
