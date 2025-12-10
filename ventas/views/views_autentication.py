from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from ..funciones.formularios import (
    RegistrationForms, LoginForm, AdminUserCreateForm, AdminUserEditForm,
    PasswordResetRequestForm, PasswordResetConfirmForm
)
from ..models.usuarios import Usuarios, Roles

# ================================================================
# =                    VISTA: LANDING PAGE                       =
# ================================================================
# 
# Esta es la página principal que verán los visitantes cuando
# accedan a la raíz del sitio ("/").
# 
# PERSONALIZACIÓN:
# - Puedes pasar datos adicionales en el contexto si necesitas
#   mostrar información dinámica (ej: productos destacados)
# - Por ahora es una página estática con el template landing.html

def home(request):
    """
    Vista para la landing page principal del sitio.
    
    Esta página muestra:
    - Hero section con imagen/video de fondo
    - Sección "Sobre Nosotros" con la historia de La Forneria Emporio
    - Footer con información de contacto, horarios y redes sociales
    
    Args:
        request: HttpRequest de Django
    
    Returns:
        HttpResponse: Renderiza el template landing.html
    """
    contexto = {
        # Contexto vacío - toda la información está en el template
    }
    
    return render(request, 'landing.html', contexto)

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

            form.add_error(None, 'Usuario o contraseña incorrectos.')
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
    """
    Vista del dashboard principal.
    
    Genera alertas automáticamente al cargar el dashboard para:
    - Productos por vencer
    - Stock bajo
    - Facturas vencidas o por vencer
    """
    from ventas.models import Alertas
    
    # Generar alertas automáticamente al cargar el dashboard
    try:
        Alertas.generar_alertas_automaticas()
    except Exception as e:
        # Si falla la generación de alertas, no bloquear la carga del dashboard
        import logging
        logger = logging.getLogger('ventas')
        logger.error(f'Error al generar alertas automáticas en dashboard: {str(e)}', exc_info=True)
    
    return render(request, 'dashboard.html')

def proximamente_view(request, feature=None):
    titulo = "En construcción" if not feature else f"{feature.replace('-', ' ').title()} en construcción"
    contexto = {
        "title": titulo,
        "message": "Estamos trabajando en esta sección. Pronto estará disponible.",
        "primary_action_url": "/",
        "primary_action_text": "Volver al inicio",
        "secondary_action_text": "Ir al dashboard",
    }
    return render(request, "proximamente.html", contexto)

def recuperar_contrasena_view(request):
    """
    Vista para solicitar recuperación de contraseña.
    El usuario ingresa su email y se le envía un enlace con token.
    """
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                
                # Generar token seguro
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Crear URL de recuperación
                # Si SITE_URL está configurado, usarlo; si no, usar request.build_absolute_uri()
                if settings.SITE_URL:
                    # En producción: usar la URL base configurada
                    reset_url = f"{settings.SITE_URL.rstrip('/')}/recuperar-contrasena/confirmar/{uid}/{token}/"
                else:
                    # En desarrollo: usar la URL de la request actual
                    reset_url = request.build_absolute_uri(
                        f'/recuperar-contrasena/confirmar/{uid}/{token}/'
                    )
                
                # Renderizar template de email
                email_subject = 'Recuperación de Contraseña - Fornería'
                email_body = render_to_string('emails/password_reset.html', {
                    'user': user,
                    'reset_url': reset_url,
                    'site_name': 'Fornería',
                })
                
                # Enviar email
                try:
                    send_mail(
                        email_subject,
                        '',  # Versión texto plano (vacía, usamos HTML)
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        html_message=email_body,
                        fail_silently=False,
                    )
                    messages.success(
                        request,
                        'Se ha enviado un correo electrónico con las instrucciones para recuperar tu contraseña. '
                        'Por favor, revisa tu bandeja de entrada.'
                    )
                    return redirect('login')
                except Exception as e:
                    messages.error(
                        request,
                        f'Error al enviar el correo electrónico: {str(e)}. '
                        'Por favor, contacta al administrador.'
                    )
            except User.DoesNotExist:
                # Por seguridad, no revelamos si el email existe o no
                messages.success(
                    request,
                    'Si el correo electrónico existe en nuestro sistema, recibirás un email con las instrucciones.'
                )
                return redirect('login')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'recuperar_contrasena.html', {'form': form})

def recuperar_contrasena_confirmar_view(request, uidb64, token):
    """
    Vista para confirmar el token y permitir cambiar la contraseña.
    """
    try:
        # Decodificar el UID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    # Verificar token
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = PasswordResetConfirmForm(request.POST)
            if form.is_valid():
                # Cambiar la contraseña
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()
                
                messages.success(
                    request,
                    'Tu contraseña ha sido restablecida exitosamente. '
                    'Ahora puedes iniciar sesión con tu nueva contraseña.'
                )
                return redirect('login')
        else:
            form = PasswordResetConfirmForm()
        
        return render(request, 'recuperar_contrasena_confirmar.html', {
            'form': form,
            'valid_token': True
        })
    else:
        # Token inválido o expirado
        messages.error(
            request,
            'El enlace de recuperación es inválido o ha expirado. '
            'Por favor, solicita un nuevo enlace.'
        )
        return redirect('recuperar_contrasena')

def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('login')

# NUEVO: gestión de usuarios (solo superusuario)

def _es_superusuario(u):
    return u.is_superuser

@login_required
@user_passes_test(_es_superusuario)
def usuarios_list_view(request):
    usuarios = User.objects.all().order_by('-is_superuser', '-is_staff', 'username')
    # Obtener perfiles Usuarios para mostrar roles
    usuarios_con_perfiles = []
    for u in usuarios:
        try:
            perfil = Usuarios.objects.get(user=u)
            usuarios_con_perfiles.append({
                'user': u,
                'perfil': perfil
            })
        except Usuarios.DoesNotExist:
            usuarios_con_perfiles.append({
                'user': u,
                'perfil': None
            })
    return render(request, 'usuarios_list.html', {'usuarios_con_perfiles': usuarios_con_perfiles})

@login_required
@user_passes_test(_es_superusuario)
def usuario_crear_view(request):
    if request.method == 'POST':
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Crear o actualizar el perfil de Usuarios
            rol = form.cleaned_data.get('rol')  # Ya es un objeto Roles, no un ID
            run = form.cleaned_data.get('run')
            
            if rol:
                Usuarios.objects.create(user=user, run=run or '', roles=rol, direccion=None)
            else:
                Usuarios.objects.create(user=user, run=run or '', direccion=None)

            messages.success(request, "Usuario creado correctamente.")
            return redirect('usuarios_list')
    else:
        form = AdminUserCreateForm()
    return render(request, 'usuario_crear.html', {'form': form})

@login_required
@user_passes_test(_es_superusuario)
def usuario_editar_view(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    
    # Obtener rol actual del usuario
    rol_actual = None
    try:
        perfil = Usuarios.objects.get(user=usuario)
        rol_actual = perfil.roles
    except Usuarios.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save()
            nueva = form.cleaned_data.get('password')
            if nueva:
                usuario.set_password(nueva)
                usuario.save()
            
            # Actualizar perfil Usuarios con el rol
            rol = form.cleaned_data.get('rol')  # Ya es un objeto Roles, no un ID
            try:
                perfil = Usuarios.objects.get(user=usuario)
                perfil.roles = rol  # Puede ser None o un objeto Roles
                perfil.save()
            except Usuarios.DoesNotExist:
                # Si no existe perfil, crearlo
                Usuarios.objects.create(user=usuario, run='', roles=rol, direccion=None)
            
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect('usuarios_list')
    else:
        form = AdminUserEditForm(instance=usuario)
        # Inicializar el campo rol con el valor actual
        if rol_actual:
            form.fields['rol'].initial = rol_actual.id
    
    return render(request, 'usuario_editar.html', {'form': form, 'usuario': usuario})

@login_required
@user_passes_test(_es_superusuario)
def usuario_eliminar_view(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    if usuario == request.user:
        messages.error(request, "No puedes eliminar tu propio usuario mientras estás conectado.")
        return redirect('usuarios_list')
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, "Usuario eliminado.")
        return redirect('usuarios_list')
    return render(request, 'confirmar_eliminar_usuario.html', {'usuario': usuario})
    
