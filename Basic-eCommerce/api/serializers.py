from rest_framework import serializers
from product.models import Product, Category
from siteSetting.models import SiteSetting
from blogs.models import Blogs

# Serializer for Products model
class ProductsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_category_name(self, obj):
        return obj.category.id if obj.category else None

# Serializer for Category model 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Site Information Serializer
class SiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = '__all__'

# Blog Serializer
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = '__all__' 
