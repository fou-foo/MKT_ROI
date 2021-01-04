from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

# modelo para asignarle tipo a los usuarios 
class Perfil(models.Model):
    TYPE_CHOICES = (
        ('medios_off_line','medios_off_line'),
        ('medios_en_tienda', 'medios_en_tienda'), 
        ('e-marketing', 'e-marketing'), 
        ('relaciones_publicas', 'relaciones_publicas'),
        ('mercadotecnia', 'mercadotecnia'), 
        ('medicion_digital', 'medicion_digital'), 
        ('mkt_digital', 'mkt_digital') )
    tipo = models.CharField(max_length=25, choices=TYPE_CHOICES, unique=True, null=True, blank=True, default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class MKTOffLine(models.Model):
    #owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # nunca borremos usuarios 
    campaña = models.CharField(max_length=60, null=False)
    objetivo_macro = models.CharField(max_length=60, null=False)
    #unidad_de_negocio = models.CharField(max_length=60, null=False)
    segmento = models.CharField(max_length=60, null=False)
    canal = models.CharField(max_length=60, null=False)
    subnanal = models.CharField(max_length=60, null=False)
    inicio = models.DateTimeField('Fecha de inicio de la campaña')
    fin = models.DateTimeField('Fecha de fin de la campaña')
    gasto = models.FloatField()
    #created = models.DateTimeField(auto_now_add=True)
    #updated = models.DateTimeField(auto_now=True)
    
