from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from ..funciones.formularios import RegistrationForms, LoginForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            entrada = form.cleaned_data['username']   # puede ser correo o username
            password = form.cleaned_data['password']

            # Si es correo, buscar el usuario y obtener su username
            if '@' in entrada:
                try:
                    usuario_obj = User.objects.get(email=entrada.lower())
                    username_para_auth = usuario_obj.username
                except User.DoesNotExist:
                    form.add_error('username', 'Este correo no está registrado.')
                    return render(request, 'login.html', {'form': form})
            else:
                username_para_auth = entrada

            # Autenticar con username y password
            user = authenticate(request, username=username_para_auth, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')

            form.add_error(None, 'Credenciales incorrectas.')
            return render(request, 'login.html', {'form': form})

        # Form inválido: re-render con errores
        return render(request, 'login.html', {'form': form})

    # GET: mostrar formulario vacío
    form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    
    if request.method == 'POST':
        form = RegistrationForms(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = User.objects.create_user(username=username, email=email, password=password)

            messages.success(request, "Cuenta creada con exito")
            return redirect('login')

    else:
        form = RegistrationForms()

    return render(request, 'registro.html', {'form': form})   


def dashboard_view(request):
    return render(request, 'dashboard.html')
    
