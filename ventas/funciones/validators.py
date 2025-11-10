import re
from django.core.exceptions import ValidationError

# Aquí definimos una función que acepta un parámetro value 
# que será el texto que queremos limpiar.
def sanitizador_texto(value):
    """
    Limpia un texto eliminando epacios extra al inicio, medio y final
    """
    if value is None:
        return None # Si no hay valor no hacemo nada

    # elimina espacion al final y inicio
    value_strip = value.strip()

    # divide el texto por los espacios y vuelve a unirlo con un solo espacio
    value_sin_espacios = ' '.join(value_strip.split())
    
    return value_sin_espacios

def validador_nombre(value, field_label="Nombre"):
    """
    No puede estar vacío.
    No puede contener caracteres de HTML ('<' o '>').
    Permite letras (incluyendo acentos), espacios, apóstrofos y guiones.
    Debe tener entre 2 y 100 caracteres.
    """ 

    # Limpiamos el texto de espacios extra
    value = sanitizador_texto(value)

    # Revismos que no este vacio
    if not value:
        raise ValidationError(f"{field_label} no puede estar vacío.")

    # Revisamos que no tenga codigo de html
    if "<" in value or ">" in value:
        raise ValidationError(f"Caracteres no permitidos en {field_label}.")

   # filtramos caracteres  y la longitud
    if not re.fullmatch(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s'-]{2,100}$", value):
        raise ValidationError(f"{field_label} solo puede contener letras, maximo 100 caracteres")

    # si todo esta bien devolvemos con el return
    return value

def validador_correo(value):
    """
    Valida el campo de correo:
    No puede star vacio
    No puede contenet caracteres de html <>
    Debe tener un formato valido usuario@dominio.com
    Hacer que este en minuscula
    """    
    # limpiar espacios extra
    valor_limpio = sanitizador_texto(value)

    # verificar que no este vacio
    if not valor_limpio:
        raise ValidationError("El correo no puede estar vacío.")

    # Bloquear intentos de html/xss
    if "<" in valor_limpio or ">" in valor_limpio:
        raise ValidationError("Caracteres no permitidos en el correo.")

    # Validar el patron estandar de email
    patron_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.fullmatch(patron_email, valor_limpio):
        raise ValidationError("Formato de correo electrónico inválido.")
    
    # devolver en minusculas
    correo_minuscula = valor_limpio.lower()
    return correo_minuscula

def validador_usuario(value):
    """
    Valida nombre de usuario
    No puede estar vacio
    No puede contener caracteres de html/xss
    Caracteres permitidos . _ -
    longitud maximo 50
    """
    # Limpiamos el texto de espacios extra
    value = sanitizador_texto(value)

    # Revismos que no este vacio
    if not value:
        raise ValidationError("El nombre de usuario no puede estar vacío.")

    # Revisamos que no tenga codigo de html
    if "<" in value or ">" in value:
        raise ValidationError("Caracteres no permitidos en el nombre de usuario.")

    # filtramos caracteres  y la longitud
    if not re.fullmatch(r"^[a-zA-Z0-9._-]{2,50}$", value):
        raise ValidationError("El nombre de usuario solo puede contener letras, números, puntos, guiones y guiones bajos, y debe tener entre 2 y 50 caracteres.")

    # si todo esta bien devolvemos con el return
    return value

def validador_contrasena_login(value):
    """
    Valida contraseña para LOGIN:
    - Obligatoria.
    - No espacios.
    - No caracteres de HTML '<' o '>'.
    - No se modifica el valor (no se aplican 'strip' ni sanitización).
    """
    if value is None or value == "":
        raise ValidationError("La contraseña es requerida.")

    if "<" in value or ">" in value:
        raise ValidationError("Caracteres no permitidos en la contraseña.")

    if " " in value:
        raise ValidationError("La contraseña no debe contener espacios.")

    return value

def validador_contrasena_registro(value):
    """
    Valida contraseña para REGISTRO:
    - Obligatoria.
    - Mínimo 8 caracteres.
    - Debe incluir letras y números.
    - Sin espacios y sin '<' o '>'.
    - Permite símbolos seguros: @#$%^&*()_-+=.!?;:,
    """
    if value is None or value == "":
        raise ValidationError("La contraseña es requerida.")

    if "<" in value or ">" in value:
        raise ValidationError("Caracteres no permitidos en la contraseña.")

    if " " in value:
        raise ValidationError("La contraseña no debe contener espacios.")

    if len(value) < 8:
        raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

    if not re.search(r"[A-Za-z]", value):
        raise ValidationError("La contraseña debe incluir letras.")

    if not re.search(r"[0-9]", value):
        raise ValidationError("La contraseña debe incluir números.")

    # Restringimos a un conjunto de símbolos comunes y seguros.
    if not re.fullmatch(r"[A-Za-z0-9@#$%^&*()_\-+=.!?;:,]{8,128}", value):
        raise ValidationError("La contraseña contiene caracteres no permitidos.")

    return value
