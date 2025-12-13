# 👤 Cómo Verificar y Crear Superusuario (Admin) en Django

## 📋 Resumen

Esta guía te explica cómo verificar si ya tienes un superusuario (admin) y cómo crearlo si no existe.

---

## 🔍 VERIFICAR SI YA TIENES SUPERUSUARIO

### Método 1: Desde la Base de Datos (MySQL)

#### En phpMyAdmin:
1. Abre phpMyAdmin: `http://localhost/phpmyadmin`
2. Selecciona la base de datos `forneria`
3. Selecciona la tabla `auth_user`
4. Haz clic en **"Examinar"**
5. Busca la columna `is_superuser`
6. Si hay algún registro con `is_superuser = 1`, **ya tienes un superusuario**

#### En línea de comandos:
```sql
USE forneria;
SELECT id, username, email, is_superuser, is_staff, is_active 
FROM auth_user 
WHERE is_superuser = 1;
```

**Si hay resultados**: Ya tienes superusuario(s)  
**Si no hay resultados**: Necesitas crear uno

---

### Método 2: Intentar Acceder al Admin de Django

1. Inicia el servidor Django:
   ```bash
   python manage.py runserver
   ```

2. Abre en el navegador:
   - `http://127.0.0.1:8000/admin`

3. Si te pide login:
   - **Ya existe el admin**, solo necesitas las credenciales
   - Si no recuerdas las credenciales, puedes crear un nuevo superusuario

4. Si te muestra error o no carga:
   - Probablemente no hay superusuario aún

---

### Método 3: Desde la Shell de Django

```bash
python manage.py shell
```

Luego ejecuta:
```python
from django.contrib.auth.models import User

# Ver todos los usuarios
usuarios = User.objects.all()
print(f"Total usuarios: {usuarios.count()}")

# Ver solo superusuarios
superusuarios = User.objects.filter(is_superuser=True)
print(f"Total superusuarios: {superusuarios.count()}")

# Listar superusuarios
for user in superusuarios:
    print(f"Username: {user.username}, Email: {user.email}, Activo: {user.is_active}")

# Salir
exit()
```

---

## ➕ CREAR SUPERUSUARIO (Si no existe)

### Método 1: Comando Interactivo (Recomendado) ⭐

```bash
python manage.py createsuperuser
```

Te pedirá:
1. **Username**: (ej: `admin`)
2. **Email address**: (ej: `admin@forneria.com`)
3. **Password**: (escribe una contraseña segura)
4. **Password (again)**: (confirma la contraseña)

**Ejemplo**:
```
Username: admin
Email address: admin@forneria.com
Password: ********
Password (again): ********
Superuser created successfully.
```

---

### Método 2: Desde la Shell de Django

```bash
python manage.py shell
```

Luego ejecuta:
```python
from django.contrib.auth.models import User

# Crear superusuario
admin = User.objects.create_superuser(
    username='admin',
    email='admin@forneria.com',
    password='tu_contraseña_segura_aqui'
)

print(f"Superusuario '{admin.username}' creado exitosamente")
exit()
```

---

### Método 3: Convertir Usuario Existente en Superusuario

Si ya tienes un usuario pero no es superusuario:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

# Buscar el usuario
usuario = User.objects.get(username='nombre_del_usuario')

# Convertirlo en superusuario
usuario.is_superuser = True
usuario.is_staff = True  # Necesario para acceder al admin
usuario.save()

print(f"Usuario '{usuario.username}' ahora es superusuario")
exit()
```

---

## 🔐 ACCEDER AL ADMIN DE DJANGO

Una vez que tengas un superusuario:

1. **Inicia el servidor**:
   ```bash
   python manage.py runserver
   ```

2. **Abre en navegador**:
   - `http://127.0.0.1:8000/admin`

3. **Inicia sesión con**:
   - **Username**: El que creaste (ej: `admin`)
   - **Password**: La contraseña que configuraste

4. ✅ Deberías ver el panel de administración de Django

---

## 📊 VERIFICAR PERMISOS DEL USUARIO

### Desde la Base de Datos:

```sql
SELECT 
    id,
    username,
    email,
    is_superuser,    -- 1 = es superusuario
    is_staff,        -- 1 = puede acceder al admin
    is_active        -- 1 = usuario activo
FROM auth_user
WHERE username = 'admin';
```

**Valores esperados para admin**:
- `is_superuser = 1` ✅
- `is_staff = 1` ✅
- `is_active = 1` ✅

---

## 🔄 CAMBIAR CONTRASEÑA DEL SUPERUSUARIO

Si olvidaste la contraseña:

```bash
python manage.py changepassword admin
```

Te pedirá:
1. **Password**: (nueva contraseña)
2. **Password (again)**: (confirma)

---

## ✅ CHECKLIST DE VERIFICACIÓN

- [ ] ✅ Verificado si existe superusuario
- [ ] ✅ Creado superusuario (si no existe)
- [ ] ✅ Puedo acceder a `/admin`
- [ ] ✅ Puedo iniciar sesión con las credenciales
- [ ] ✅ Veo el panel de administración

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "Username already exists"
**Solución**: El usuario ya existe. Puedes:
1. Usar otro username
2. O convertir el usuario existente en superusuario (Método 3)

### Error: "This field is required"
**Solución**: Asegúrate de llenar todos los campos (username, email, password)

### Error: "The two password fields didn't match"
**Solución**: Las contraseñas no coinciden. Intenta de nuevo.

### No puedo acceder a /admin
**Solución**: Verifica que:
1. El usuario tiene `is_superuser = 1`
2. El usuario tiene `is_staff = 1`
3. El usuario tiene `is_active = 1`
4. Estás usando las credenciales correctas

### "You don't have permission to access this page"
**Solución**: El usuario no es superusuario. Conviértelo usando el Método 3.

---

## 📝 NOTAS IMPORTANTES

1. **Superusuario = Admin**: Sí, el superusuario es el administrador del sistema
2. **is_superuser**: Permite acceso total al sistema
3. **is_staff**: Necesario para acceder a `/admin`
4. **is_active**: El usuario debe estar activo para poder iniciar sesión

---

## 🎯 RESUMEN RÁPIDO

```bash
# Verificar si existe
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.filter(is_superuser=True).count()

# Crear superusuario
python manage.py createsuperuser

# Cambiar contraseña
python manage.py changepassword admin
```

---

**Fecha**: Hoy  
**Estado**: ✅ **LISTO PARA USAR**

