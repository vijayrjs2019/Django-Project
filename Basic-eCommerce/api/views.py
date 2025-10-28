from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import ProductsSerializer, CategorySerializer, SiteSettingSerializer , BlogSerializer
from product.models import Product,Category
from siteSetting.models import SiteSetting
from blogs.models import Blogs

# Get all furnitures
@api_view()
def get_furnitures(request):
    productQuerySet = Product.objects.all()
    productSerializer = ProductsSerializer(productQuerySet, many=True)
     
    return Response({
        'data': productSerializer.data
    })

# Get all furnitures Details by ID
@api_view()
def get_furnitures_detail(request, product_id):
    productQuerySet = Product.objects.get(id=product_id)
    productSerializer = ProductsSerializer(productQuerySet, many=False)
    
    return Response({
        'data': productSerializer.data
    })

# Get all furnitures Details by Category ID
@api_view()
def get_furnitures_by_category(request, category_id):
    productQuerySet = Product.objects.get(category=category_id)
    productSerializer = ProductsSerializer(productQuerySet, many=False)
    
    return Response({
        'data': productSerializer.data
    })



# Get all categories
@api_view()
def get_categories(request):
    categoryQuerySet = Category.objects.all()
    categorySerializer = CategorySerializer(categoryQuerySet, many=True)
    
    return Response({
        'data': categorySerializer.data
    })

# Get all site information
@api_view()
def get_site_info(request):
    siteQuerySet = SiteSetting.objects.all()
    siteSerializer = SiteSettingSerializer(siteQuerySet, many=True)
    
    return Response({
        'data': siteSerializer.data
    })

# Get all blogs List
@api_view()
def get_blogs(request):
    blogQuerySet = Blogs.objects.all()
    blogSerializer = BlogSerializer(blogQuerySet, many=True)
    
    return Response({
        'data': blogSerializer.data
    })

@api_view()
def get_blog_detail(request, blog_id):
    blogQuerySet = Blogs.objects.get(id=blog_id)
    blogSerializer = BlogSerializer(blogQuerySet, many=False)
    
    return Response({
        'data': blogSerializer.data
    })
