from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'registro.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')
    
