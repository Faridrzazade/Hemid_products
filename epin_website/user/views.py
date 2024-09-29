from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.core.exceptions import ValidationError

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)  
        if form.is_valid():
            username = form.cleaned_data['username']
            # İstifadəçi adının daha öncə mövcud olub olmadığını yoxlayın
            if User.objects.filter(username=username).exists():
                messages.error(request, "Bu istifadəçi adı artıq mövcuddur.")
                return render(request, 'register.html', {'form': form})

            user = User.objects.create_user(
                username=username,
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']  # E-poçtu burada əlavə edin
            )
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend') 
            
            # E-poçt göndər
            send_mail(
                'Qeydiyyat uğurla tamamlandı',
                'Hesabınız uğurla yaradıldı! Zəhmət olmasa e-poçt ünvanınızı təsdiqləyin.',
                'your_email@example.com',  # Göndərən e-poçt
                [user.email],  # Alıcının e-poçtu
                fail_silently=False,
            )

            messages.success(request, 'Hesabınız uğurla yaradıldı! E-poçt təsdiqini yoxlayın.')
            return redirect('home')  # Uğurlu qeydiyyatdan sonra ana səhifəyə yönləndirin
        else:
            messages.error(request, "Formda səhv var. Zəhmət olmasa, yenidən cəhd edin.")  # Səhv mesajı əlavə edin
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "İstifadəçi adı və ya parol səhvdir")  # Səhv mesajı
            return render(request, "login.html", context)

        messages.success(request, "Uğurla giriş olundu")
        login(request, user)
        return redirect("home")

    return render(request, "login.html", context)

def logoutUser(request):
    logout(request)
    messages.success(request, "Uğurla çıxış olundu")  # Çıxış mesajı əlavə et
    return redirect('login')  # Çıxışdan sonra login səhifəsinə yönləndir
