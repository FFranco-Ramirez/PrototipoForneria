from django.db import models
from django.contrib.auth.models import User

# Modelo para los Roles de Usuario
class Roles(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'roles'

# Modelo para la Dirección
class Direccion(models.Model):
    calle = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    depto = models.CharField(max_length=10, null=True, blank=True)
    comuna = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'direccion'

# Modelo de Perfil de Usuario, extendiendo el User de Django
class Usuarios(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    run = models.CharField(max_length=10, unique=True)
    fono = models.IntegerField(null=True, blank=True)
    direccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, null=True)
    roles = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'