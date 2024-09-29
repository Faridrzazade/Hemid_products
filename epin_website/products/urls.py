from django.urls import path, include
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('', ProductListCreateView.as_view(), name='product-list'),
    path('ratings', RatingView.as_view(), name='ratings'),
    #path('search', SearchView.as_view(), name='search'),
    path('contact/', contact, name='contact'),
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('categories/', category_list, name='category_list'),
    path('categories/<int:category_id>/', category_detail, name='category_detail'),
    path('user/',include("user.urls")),
    #path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('search/', search, name='search'),
     path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
     path('signup/', signup, name='signup'),
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)