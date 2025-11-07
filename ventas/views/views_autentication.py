from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from ..funciones.formularios import RegistrationForm, LoginForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Inicio de sesión exitoso")
                return redirect('dashboard')
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def register_view(request):
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = User.objects.create_user(username=username, email=email, password=password)

            messages.success(request, "Cuenta creada con exito")
            return redirect('login')

    else:
        form = RegistrationForm()

    return render(request, 'registro.html', {'form': form})   


def dashboard_view(request):
    return render(request, 'dashboard.html')
    
