from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import ProductSerializer, RatingSerializer, CategorySerializer
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .forms import SearchForm, ContactForm
from django.contrib.auth.decorators import login_required
from allauth.account.views import SignupView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'product_list.html', {'categories': categories, 'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories/list.html', {'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'categories/detail.html', {'category': category, 'products': products})

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class RatingView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        results = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(results, many=True)
        return Response(serializer.data)

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

    return redirect('cart_detail')
 

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.total_price() for item in cart_items)
    total_items = cart_items.count()

    return render(request, 'cart_detail.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_items,
    })

   


def search(request):
    form = SearchForm()
    results = []
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.objects.filter(title__icontains=query)
    
    return render(request, 'search.html', {'form': form, 'results': results})


class CustomSignupView(SignupView):
    def get_success_url(self):
        return '/your-success-url/'
    


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # E-poçt göndərmək
        send_mail(
            'Qeydiyyat Uğurla Tamamlandı',
            'Hörmətli, qeydiyyatınız uğurla tamamlandı!',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return redirect('success_page')
    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # E-poçt göndərmə funksiyası
            send_mail(
                f'Mesaj: {name}',  # Mövzu
                message,           # Mesaj
                settings.DEFAULT_FROM_EMAIL,  # Göndərən
                [email],  # Alıcı e-poçtu
                fail_silently=False,
            )

            return render(request, 'success.html')  # Uğurlu göndərmədən sonra yönləndirmə
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})