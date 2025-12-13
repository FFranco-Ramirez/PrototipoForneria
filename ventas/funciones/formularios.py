from django import forms
from django.contrib.auth.models import User
from .validators import (
    sanitizador_texto,
    validador_usuario,
    validador_correo,
    validador_contrasena_login,
    validador_contrasena_registro,
)

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuario o Correo Electronico",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Mjfarms o trabajador@gmail.com',
                'autocomplete': 'username',
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
                'autocomplete': 'current-password',
            }
        )
    )
    
    def clean_username(self):
        """
        Este campo acepta: nombre de usuario O correo.
        1) Limpiar espacios.
        2) Si tiene '@', validar como correo.
        3) Si no, validar como usuario.
        """
        valor_original = self.cleaned_data.get('username')
        valor_limpio = sanitizador_texto(valor_original)

        if '@' in valor_limpio:
            return validador_correo(valor_limpio)
        else:
            return validador_usuario(valor_limpio)    

    def clean_password(self):
        """
        Validar contraseña para login:
        - Debe existir.
        - No espacios.
        - No '<' ni '>'.
        """
        valor_original = self.cleaned_data.get('password')
        return validador_contrasena_login(valor_original)

# --------------------------------------------------
# Formulario de registro de ususario
class RegistrationForms(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mjfarms',
            'autocomplete': 'username',
        })
    )

    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'usuario@dominio.com',
            'autocomplete': 'email',
        })
    )

    password = forms.CharField(
        label="Contraseña",
        required=True,
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'autocomplete': 'new-password',
        })
    )

    password_confirm = forms.CharField(
        label="Confirmar contraseña",
        required=True,
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña',
            'autocomplete': 'new-password',
        })
    )

# ------ Metodos ----------------

    """
    clean Este es un nombre mágico para Django cuando Django valida un formulario,
    busca métodos que empiecen con clean_ seguido del nombre de un campo.
    Como nuestro campo se llama username 
    este método se ejecutará automáticamente para validar específicamente ese campo.
    """
    def clean_username(self):
        """
        Username para registro:
        - Validar formato de usuario (no correo).
        - Verificar que no exista.
        """
        username = validador_usuario(self.cleaned_data.get('username'))
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya existe")
        return username

    def clean_email(self):
        """
        Email para registro:
        - Validar formato.
        - Verificar que no exista.
        """
        email = validador_correo(self.cleaned_data.get('email'))
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya está registrado")
        return email

    """
    Metodo que revisa que las contraseñas sean igual
    """
    def clean(self):
        """
        Pasos
        Verificar que 'password' y 'password_confirm' coincidan.
        Aplicar reglas de fuerza a 'password' en registro.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # Paso 1: confirmar contraseñas iguales
        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Las contraseñas no coinciden")
            return cleaned_data

        # Paso 2: fortalecer contraseña (si existe)
        if password:
            cleaned_data["password"] = validador_contrasena_registro(password)

        return cleaned_data

class AdminUserCreateForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la contraseña',
            'autocomplete': 'new-password',
        })
    )
    
    password_confirm = forms.CharField(
        label="Confirmar contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme la contraseña',
            'autocomplete': 'new-password',
        })
    )
    
    rol = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label="Rol",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione un rol"
    )
    
    run = forms.CharField(
        label="RUN",
        required=False,
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12345678-9'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from ..models.usuarios import Roles
        self.fields['rol'].queryset = Roles.objects.all()
        # Ocultar estos campos y establecer valores por defecto
        self.fields['is_active'].widget = forms.HiddenInput()
        self.fields['is_staff'].widget = forms.HiddenInput()
        self.fields['is_superuser'].widget = forms.HiddenInput()
        self.fields['is_active'].initial = True
        self.fields['is_staff'].initial = True
        self.fields['is_superuser'].initial = False

    def clean_username(self):
        username = validador_usuario(self.cleaned_data.get('username'))
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya existe")
        return username

    def clean_email(self):
        email = validador_correo(self.cleaned_data.get('email'))
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya está registrado")
        return email

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password_confirm

    def clean_first_name(self):
        valor = sanitizador_texto(self.cleaned_data.get('first_name') or '')
        return valor

    def clean_last_name(self):
        valor = sanitizador_texto(self.cleaned_data.get('last_name') or '')
        return valor

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        if pwd:
            return validador_contrasena_registro(pwd)
        return pwd

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

# ================================================================
# =        FORMULARIOS PARA RECUPERACIÓN DE CONTRASEÑA          =
# ================================================================

class PasswordResetRequestForm(forms.Form):
    """
    Formulario para solicitar recuperación de contraseña.
    Solo requiere el email del usuario.
    """
    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su correo electrónico',
            'autocomplete': 'email',
        })
    )
    
    def clean_email(self):
        email = validador_correo(self.cleaned_data.get('email'))
        # Verificar que el email exista en la base de datos
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "No existe una cuenta asociada a este correo electrónico."
            )
        return email

class PasswordResetConfirmForm(forms.Form):
    """
    Formulario para confirmar y establecer nueva contraseña.
    Requiere nueva contraseña y confirmación.
    """
    new_password = forms.CharField(
        label="Nueva contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su nueva contraseña',
            'autocomplete': 'new-password',
        })
    )
    
    new_password_confirm = forms.CharField(
        label="Confirmar nueva contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme su nueva contraseña',
            'autocomplete': 'new-password',
        })
    )
    
    def clean_new_password(self):
        password = self.cleaned_data.get('new_password')
        if password:
            return validador_contrasena_registro(password)
        return password
    
    def clean_new_password_confirm(self):
        password = self.cleaned_data.get('new_password')
        password_confirm = self.cleaned_data.get('new_password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password_confirm

class AdminUserEditForm(forms.ModelForm):
    password = forms.CharField(
        label="Nueva contraseña",
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dejar vacío para no cambiar',
            'autocomplete': 'new-password',
        })
    )
    
    rol = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label="Rol",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione un rol"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from ..models.usuarios import Roles
        self.fields['rol'].queryset = Roles.objects.all()

    def clean_username(self):
        username = validador_usuario(self.cleaned_data.get('username'))
        existe = User.objects.filter(username=username).exclude(pk=self.instance.pk).exists()
        if existe:
            raise forms.ValidationError("El nombre de usuario ya existe")
        return username

    def clean_email(self):
        email = validador_correo(self.cleaned_data.get('email'))
        existe = User.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
        if existe:
            raise forms.ValidationError("El correo electrónico ya está registrado")
        return email

    def clean_first_name(self):
        valor = sanitizador_texto(self.cleaned_data.get('first_name') or '')
        return valor

    def clean_last_name(self):
        valor = sanitizador_texto(self.cleaned_data.get('last_name') or '')
        return valor

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        if pwd:
            return validador_contrasena_registro(pwd)
        return pwd
