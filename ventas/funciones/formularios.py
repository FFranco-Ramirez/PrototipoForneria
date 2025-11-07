from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form): # importamos por herencia de forms.Form que son validadores por defecto que te da django
    username = forms.CharField(
        label="Usuario o Correo Electronico",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Mjfarms o trabajador@gmail.com',
            }
        )
    )
    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña',
            }
        )
    )
# --------------------------------------------------
# Formulario de registro de ususario
class RegistrationForms(forms.Form):
    
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=50,
        required=True,        
    )

    email = forms.EmailField(
        label="Correo electronico",
        required=True,
        max_length=100,
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        required=True,
        max_length=128,
    )

    password_confirm = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
        required=True,
        max_length=128,
    )

# ------ Metodos ----------------

    """
    clean Este es un nombre mágico para Django cuando Django valida un formulario,
    busca métodos que empiecen con clean_ seguido del nombre de un campo.
    Como nuestro campo se llama username 
    este método se ejecutará automáticamente para validar específicamente ese campo.
    """
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya existe")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya está registrado")
        return email

    """
    Metodo que revisa que las contraseñas sean igual
    """
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Las contraseñas no coinciden")
        
        return cleaned_data
