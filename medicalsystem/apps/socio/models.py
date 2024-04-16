# ----------- Importaciones -----------
from django.db import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
# ----------- FIN Importaciones -----------


# ------------------- Modelo Telefono -----------------------------

class Telefono(models.Model):
    numero_de_telefono = models.CharField(max_length=20, verbose_name='Número de contacto')
    numero_de_telefono2 = models.CharField(max_length=20, blank=True, null=True, verbose_name='Número de contacto 2')

    class Meta:
        verbose_name = 'Telefono'
        verbose_name_plural = 'Registro de Telefonos'

    def __str__(self):
        return f"{self.numero_de_telefono}"
    
# ------------------- FIN Modelo Telefono -----------------------------

    
# ----------- Modelo "PACIENTE" -----------
class Paciente(models.Model):

    # ------ El tipo de categoría es basada en el tipo de atención ------
    #(0) Demanda Espontánea -> Primera vez de la persona, no cuenta con documentación para asociarlo.
    #(1) Socio -> Persona recurrente, se asocia con DNI pero no tiene obra social o monitributo.
    #(2) Socio Afiliado -> Persona ya asociada con DNI, cuenta con monotributo u obra social.
    TIPO_CATEGORIA = (
        ('0', 'Demanda Espontánea'),
        ('1', 'Socio'),
        ('3', 'Socio Afiliado')
    )

    # Género de la persona
    SEX_CHOICES = (
        ('0', 'Masculino'),
        ('1', 'Femenino'),
        ('3', 'Otro')
    )

    # El tipo de solicitud es el rol del paciente en grupo familiar.
    # (0) Titular -> Si es mayor de 18 años
    # (1) Familiar -> Debe ser familiar de alguien ya asociado, por ejemplo el hijo u hija de un Titular.
    # (2) No Aplica -> En casos donde no se puede categorizar ya sea porque se atiende un menor sin acompañamiento de un mayor u otros casos.
    TIPO_SOLICITUD = (
        ('0', 'Titular'),
        ('1', 'Familiar'),
        ('2', 'No Aplica'),
    )


    # Tipo de monitributo del paciente si es que tiene, en caso de que no tenga opción (5).
    TIPO_MONOTRIBUTO = (
        ('0', 'Categoria A'),
        ('1', 'Categoria B'),
        ('2', 'Categoria C'),
        ('3', 'Categoria D'),
        ('4', 'Otro'),
        ('5', 'No tiene'),
    )

    # ------------------- CAMPOS DE LA TABLA PACIENTE -----------------------------
    categoria = models.CharField('Categoria', max_length=1, choices=TIPO_CATEGORIA, default='0') 
    condicion_de_solicitud = models.CharField('Condición de solicitud', max_length=1, choices=TIPO_SOLICITUD, default='0')
    dni = models.CharField(max_length=8, unique=True, verbose_name='DNI',help_text="<span style='color: red;font-weight: bold; text-transform: uppercase;'>¡Ingresar sin caracteres especiales o espacios ( - , * , _, . )!</span>")
    dnititular = models.CharField('DNI del Titular',max_length=8, blank=True, null=True, help_text="<span style='color: red;font-weight: bold; text-transform: uppercase;'>¡Colocar unicamente si el TIPO DE AFILIACIÓN ES FAMILIAR!</span>")
    cuit = models.CharField(max_length=20, blank=True, null=True, help_text="<span style='color: red;font-weight: bold; text-transform: uppercase;'>¡Ingresar sin caracteres especiales o espacios ( - , * , _ )!</span>", verbose_name='CUIT')  # Campo opcional
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_de_nacimiento = models.DateField()
    sex = models.CharField('Sexo', max_length=1, choices=SEX_CHOICES, default='0')
    telefono = models.ForeignKey(Telefono, on_delete=models.CASCADE, verbose_name='Número de contacto', blank=True, null=True)
    casilla_de_mail = models.EmailField(validators=[EmailValidator(message="Ingresa un correo válido")], blank=True)
    domicilio = models.ForeignKey('Domicilio', on_delete=models.SET_NULL, blank=True, null=True)
    referente_parroquial = models.ForeignKey('Referente', on_delete=models.SET_NULL, blank=True, null=True)
    responsable_de_carga = models.ForeignKey('auth.User', on_delete=models.SET_NULL, blank=True, null=True, editable=False)
    monotributo = models.CharField('Monotributo', max_length=1, choices=TIPO_MONOTRIBUTO, default='0')
    dni_foto_frente = models.FileField(upload_to='dni/', blank=True, null=True)
    dni_foto_dorso = models.FileField(upload_to='dni/', blank=True, null=True)
    credencial = models.AutoField(primary_key=True)
    observaciones = models.TextField(blank=True)
    credencial_entregada = models.BooleanField(default=False)
    
     # ------------------- FIN CAMPOS DE LA TABLA PACIENTE -----------------------------
    
    # Ajustes visuales
    class Meta:
        verbose_name = 'Socio' # Titulo.
        verbose_name_plural = 'Registro de socios' # Titulo Plural.

    # ----------- Funciones -----------
    
    #Valida que el campo "DNI DEL TITULAR" este completado en caso de que se este asociando un "Familiar". | En caso de que no sea un "Familiar" no se ejecuta la función.
    def clean(self):
        if self.condicion_de_solicitud == '1' and not self.dnititular:
            raise ValidationError("El campo 'DNI del Titular' es obligatorio para el tipo de afiliación 'Familiar'.")
        # Validación 2 (FAMILIAR) -> Si se coloca el  "DNI DEL TITULAR", verifica que realmente ese DNI corresponda a un paciente asociado.
        if self.condicion_de_solicitud == '1' and self.dnititular:
            if Paciente.objects.filter(dni=self.dnititular, condicion_de_solicitud='0').count() == 0:
                raise ValidationError("El 'DNI del Titular' especificado no existe en el Sistema.")

    # Función -> Se encarga de calcular la edad tomando la fecha de nacimiento y la fecha actual, se realiza una operación matematica para calcular la edad.
    def calcular_edad(self):
        today = timezone.now().date()
        age = today.year - self.fecha_de_nacimiento.year - ((today.month, today.day) < (self.fecha_de_nacimiento.month, self.fecha_de_nacimiento.day))
        return age

    # Función que devuelve unicamente el apellido y nombre del paciente.
    def __str__(self):  
        return f"{self.apellidos}, {self.nombres}"

# ---------------------- FIN Modelo "PACIENTE" ----------------------



# ---------------------- Modelo "Tipo de certificado" ----------------------

class TipoCertificado(models.Model):
    Tipo = models.CharField('Tipo de certificado', max_length=100)
    descripcion = models.CharField('Descripción', max_length=50)
    class Meta:
        verbose_name = 'Tipo de certificado'
        verbose_name_plural = 'Tipos de certificado'


    def __str__(self):  
        return f"{self.Tipo}"
    
# ---------------------- FIN Modelo "Tipo de certificado" ----------------------
    



# ---------------------- Modelo "Certificado" ----------------------

class Certificado(models.Model):
    certificado = models.FileField(upload_to='certificados/')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tipocertificado = models.ForeignKey(TipoCertificado, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Registro de certificados'


    def __str__(self):  
        return f"{self.paciente}, {self.tipocertificado}"

 # ---------------------- FIN Modelo "Certificado" ----------------------




# ---------------------- Modelo "Domicilio" ----------------------
class Domicilio(models.Model):
    calle = models.CharField(max_length=100, verbose_name='Domicilio')
    numero = models.CharField(max_length=10, blank=True, default='S/N')
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    localidad = models.CharField(max_length=100)
    partido = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Domicilio'
        verbose_name_plural = 'Registro de Domicilios'

    # ----------- Funciones -----------
    def __str__(self):
        return f"{self.calle} {self.numero}, {self.localidad}"

# ---------------------- FIN Modelo "Domicilio" ----------------------



# ---------------------- Modelo "Referente Parroquial" ----------------------
class Referente(models.Model):
    apellidos = models.CharField(max_length=100, blank=True)
    nombres = models.CharField(max_length=100, blank=True)
    alias = models.CharField(max_length=100)
    parroquia = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Referente Parroquial'
        verbose_name_plural = 'Registro de Referentes'

    def __str__(self):
        return f"{self.alias}"

# ---------------------- FIN Modelo "Referente Parroquial" ----------------------
