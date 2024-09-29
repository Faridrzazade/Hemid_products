"""
URL configuration for epin_website project.

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
from django.urls import path, include
from products.views import *
from products import views
from products.forms import SearchForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),  # Əsas URL-lər üçün `products.urls` faylını daxil edin
    #path('products/', product_list_view, name='product_list'),
    path('api/products/', ProductListCreateView.as_view(), name='api-product-list'),  # DRF üçün ayrıca URL
    path('api/products/<int:pk>/', ProductDetailView.as_view(), name='api-product-detail'),  # DRF üçün ayrıca URL
    path('api/ratings/', RatingView.as_view(), name='api-ratings'),  # DRF üçün ayrıca URL
    path('api/search/', SearchView.as_view(), name='api-search'),
    path('cart/', include('shopping_cart.urls')),
    path('user/',include("user.urls")),
]