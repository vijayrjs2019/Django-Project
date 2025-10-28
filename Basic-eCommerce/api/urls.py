"""
URL configuration for dj_18 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from dj_18 import views
from api import views

urlpatterns = [
    path('get-site-info/', views.get_site_info, name='get_site_info'),
    path('get-categories/', views.get_categories, name='get_categories'),
    path('get-furnitures/', views.get_furnitures, name='get_furnitures'),
    path('get-furnitures-detail/<int:product_id>', views.get_furnitures_detail, name='get_furnitures_detail'),
    path('get-furnitures-by-category/<int:category_id>', views.get_furnitures_by_category, name='get_furnitures_by_category'),
    path('get-blogs/', views.get_blogs, name='get_blogs'),
    path('get-blog-detail/<int:blog_id>', views.get_blog_detail, name='get_blog_detail'),
]
 